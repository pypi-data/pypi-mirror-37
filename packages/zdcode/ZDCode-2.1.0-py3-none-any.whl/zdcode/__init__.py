import re
import textwrap
import zdcode.zdlexer



actor_list = {}


def decorate(o, *args, **kwargs):
    """Get the object's compiled DECORATE code."""
    # print("Getting DECORATE code for a {}...".format(type(o).__name__))
    return o.__decorate__(*args, **kwargs)

def big_lit(s, indent=4, tab_size=4, strip_borders=True):
    """This function assists in the creation of
fancier triple-quoted literals, by removing
trailing indentation in lines and trailing
and leading spaces/newlines from formatting."""

    if s == "":
        return ""

    while s[0] in "\n\r": s = s[1:]
    while s[-1] in "\n\r": s = s[:-1]
    if strip_borders: s = s.strip(" \t")
    lines = s.splitlines()
    result = []

    for l in lines:
        i = indent
        while i > 0:
            if l.startswith("\t"):
                i -= tab_size
                l = l[1:]

            elif l.startswith(" "):
                i -= 1
                l = l[1:]

            else:
                break

        result.append(l)

    result = "\n".join(result)
    return result

assert big_lit("""
    YAY! I am
        Working!
""", 8) == "YAY! I am\nWorking!"

assert big_lit("""
    YAY! I am
        Working!
""", 4) == "YAY! I am\n    Working!"

assert big_lit("""
    Big
        Fluffy
    Furry.

    """, 4) == "Big\n    Fluffy\nFurry.\n"

def redent(code, spaces=8, unindent_first=True):
    b = textwrap.dedent(code).splitlines()
    r = []

    for l in b:
        r.append((" " * spaces) + l)

    r = "\n".join(r)

    if unindent_first:
        return r.lstrip("\t ")

    return r

# ZDCode Classes
class ZDProperty(object):
    def __init__(self, code, name, value):
        self.code = code
        self.name = name
        self.value = value

        self.code.properties[name] = self

    def __decorate__(self):
        return "    {} {}".format(self.name, self.value)

class ZDCall(object):
    def __init__(self, code, label, func, args=None, repeats=1):
        if not args:
            args = []

        repeats = int(repeats)

        self.func = func
        self.code = code
        self.args = args
        self.label = label
        self.actor = label._actor
        self.repeats = repeats

        self.id = len(code.calls)
        code.calls.append(self)
        label.states.append(self)

        if repeats > 1:
            for _ in range(repeats):
                ZDCall(code, label, func, args, 1)

            del self

        elif "_Call{}".format(self.id) not in [x.name for x in code.inventories]:
            ZDInventory(code, "_Call{}".format(self.id))

    def post_load(self):
        if self.func in self.actor.namefuncs:
            self.actor.namefuncs[self.func].add_call(self)

    def num_states(self):
        return 2 + 2 * len(self.actor.namefuncs[self.func].args)
            
    def add_arg(self, a):
        self.args.append(a)

    def __decorate__(self):
        r = ""
        func = self.actor.namefuncs[self.func]

        for i, a in enumerate(self.args):
            r += "    TNT1 A 0 A_TakeInventory(\"{0}\")\n    TNT1 A 0 A_GiveInventory(\"{0}\", {1})\n".format(func.args[i], a)

        return r + "    TNT1 A 0 A_GiveInventory(\"_Call{1}\")\n    Goto F_{0}\n_CLabel{1}:\n    TNT1 A 0 A_TakeInventory(\"_Call{1}\")".format(func.name, self.id)

class ZDFunction(object):
    def __init__(self, code, actor, name, args=None, states=None):
        if not args:
            args = []

        if not states:
            states = []

        self.code = code
        self.name = name
        self.states = states
        self.calls = []
        self.actor = actor
        self.args = args

        self.id = len(actor.all_funcs)
        actor.funcs.append((name, self))
        actor.namefuncs[name] = self
        actor.all_funcs.append((name, self))

        for a in args:
            if a not in [x.name for x in code.inventories]:
                ZDInventory(code, a)

    def add_call(self, call):
        self.calls.append(call)

    def add_arg(self, argstr):
        self.args.append(argstr)

        for a in self.args:
            if a not in [x.name for x in self.code.inventories]:
                ZDInventory(self.code, a)

    def call_states(self):
        result = []

        for c in self.calls:
            result.append("TNT1 A 0 A_JumpIfInventory(\"_Call{0}\", 1, \"_CLabel{0}\")".format(c.id))

        return "    " + redent("\n".join(result), 4)

    def state_code(self):
        r = ""
    
        for s in self.states:
            if type(s) in (ZDState, ZDRawDecorate):
                r += "    {}\n".format(decorate(s))
            
            else:
                r += "{}\n".format(decorate(s))
            
        return r[:-1]
        
    def __decorate__(self):
        code = """    F_{}:""".format(self.name)
        code += '\n' + self.state_code()
        code += '\n' + self.call_states()

        return code

class ZDState(object):
    def __init__(self, sprite="TNT1", frame="A", duration=0, keywords=None, action=None):
        if not keywords:
            keywords = []

        self.sprite = sprite[:4]
        self.frame = frame
        self.keywords = keywords
        self.action = action
        self.duration = duration

    def num_states(self):
        return 1
        
    def __decorate__(self):
        if self.keywords:
            keywords = [" "] + self.keywords

        else:
            keywords = []

        action = ""
        if self.action:
            action = " " + str(self.action)

        return "{} {} {}{}{}".format(
            self.sprite.upper(),
            self.frame.upper(),
            str(self.duration),
            " ".join(keywords),
            action
        )

class ZDLabel(object):
    def __init__(self, _actor, name, states=None):
        if not states:
            states = []

        self.name = name
        self.states = states
        self._actor = _actor

        self._actor.labels.append(self)

    def add_state(self, state):
        self.states.append(state)

    def __decorate__(self):
        if self.name.startswith("F_"):
            self.name = "_" + self.name

        r = "{}:".format(self.name)

        for s in self.states:
            if type(s) in (ZDState, ZDRawDecorate):
                r += "\n    {}".format(decorate(s))
                
            else:
                r += "\n{}".format(decorate(s))

        return r

class ZDRawDecorate(object):
    def __init__(self, raw):
        self.raw = raw

    def __decorate__(self):
        return self.raw

class ZDActor(object):
    def __init__(self, code, name="DefaultActor", inherit=None, replace=None, doomednum=None):
        self.code = code
        self.labels = []
        self.properties = {}
        self.flags = []
        self.antiflags = []
        self.inherit = inherit
        self.name = name
        self.replace = replace
        self.num = doomednum
        self.funcs = []
        self.namefuncs = {}
        self.all_funcs = []
        self.raw = []
        
        actor_list[name] = self
        
        if inherit in actor_list:
            self.all_funcs = actor_list[inherit].all_funcs

    def top(self):
        r = []

        for p in sorted(self.properties.values(), key=lambda p: p.name):
            r.append(decorate(p))

        r.append("")

        for f in self.flags:
            r.append("+{}".format(f))

        for a in self.antiflags:
            r.append("-{}".format(a))

        for rd in self.raw:
            r.append(rd)

        if len(r) == 1 and r[0] == "":
            return "    \n"
            
        return redent(big_lit("\n".join(r), 8), 4, False) + "\n\n\n            "

    def label_code(self):
        r = []

        for f in self.funcs:
            r.append(decorate(f[1]))

        for l in self.labels:
            r.append(decorate(l))

        return redent("\n\n".join(r), 8, False)

    def header(self):
        r = self.name

        if self.inherit: r += " : {}".format(self.inherit)
        if self.replace: r += " replaces {}".format(self.replace)
        if self.num:     r += " {}".format(str(self.num))

        return r

    def __decorate__(self):
        if self.labels + self.funcs:
            return big_lit(
            """
            Actor {}
            {{
            {}States {{
                    {}
                }}
            }}""", 12).format(self.header(), redent(self.top(), 4, unindent_first=False), redent(self.label_code(), unindent_first=True))

        return big_lit(
        """
        Actor {}
        {{
        {}
        }}""", 8).format(self.header(), redent(self.top(), 4, unindent_first=False))

class ZDRepeat(object):
    def __init__(self, actor, repeats, states):
        self._actor = actor
        self.states = states
        self.repeats = repeats
        
    def num_states(self):
        return sum(x.num_states() for x in self.states) * self.repeats
        
    def __decorate__(self):
        return redent('\n'.join([decorate(x) for x in self.states] * self.repeats), 4, unindent_first=False)
        
class ZDIfStatement(object):
    def __init__(self, actor, condition, states):
        self._actor = actor
        self.condition = condition
        self.states = states
            
    def num_states(self):
        return sum(x.num_states() for x in self.states) + 2
            
    def __decorate__(self):
        num_st = sum(x.num_states() for x in self.states)
    
        return redent("TNT1 A 0 A_JumpIf(!({}), {})\n".format(self.condition, num_st + 1) + '\n'.join(decorate(x) for x in self.states) + "\nTNT1 A 0", 4, unindent_first=False)
        
num_whiles = 0

class ZDWhileStatement(object):
    def __init__(self, actor, condition, states):
        global num_whiles
        
        self._actor = actor
        self.condition = condition
        self.states = states
        self.id = num_whiles
        num_whiles += 1
            
    def num_states(self):
        return sum(x.num_states() for x in self.states) + 3
            
    def __decorate__(self):
        num_st = sum(x.num_states() for x in self.states)
    
        return redent("_WhileBlock{}:\n".format(self.id) + redent("TNT1 A 0 A_JumpIf(!({}), {})\n".format(self.condition, num_st + 2) + '\n'.join(decorate(x) for x in self.states) + "\nTNT1 A 0 A_Jump(255, \"_WhileBlock{}\")\nTNT1 A 0".format(self.id), 4, unindent_first=False), 0, unindent_first=False)
        
class ZDInventory(object):
    def __init__(self, code, name):
        self.name = name
        self.code = code

        code.inventories.append(self)

    def __decorate__(self):
        return "Actor {} : Inventory {{Inventory.MaxAmount 1}}".format(self.name)
        
# Parser!
class ZDCode(object):
    class ZDCodeError(BaseException):
        pass
        
    # args = Forward()
    # args << (Combine(CharsNotIn("()") + "(" + args + ")" + Optional("," + args)) | CharsNotIn(")"))
    # inherit = Optional(":" + Word(alphanums + "_"))
    # replace = Optional("->" + Word(alphanums + "_"))
    # denum = Optional("*" + Word(nums))
    # parser = Forward()
    # st = Forward()
    # actorargs = Forward()
    # actorargs << (inherit ^ replace ^ denum) + (FollowedBy("{") | Optional(actorargs))
    # action = Group(Word(alphanums + "_-") + Optional("(" + args + ")"))
    # cond = "?" + SkipTo("==") + "==" + Word(nums) + "->" + Word(alphanums + "_-.") + ";"
    # call = "(" + Word(alphas+"_", alphanums+"_") + ")" + Optional("(" + Optional(args) + ")") + ";"
    # raw = "^" + SkipTo(";") + ";"
    # normstate = Word(alphanums + "_-", exact=4) + Word(alphas + "[]") + Word(nums) + ZeroOrMore(Group("[" + SkipTo("]") + "]")) + Optional("@" + action) + ";"
    # state = Optional("*" + Word(nums)) + ":" + (cond ^ call ^ raw ^ normstate)
    # flagname = Word(alphanums + "_.")
    # flag = "*" + flagname + ";"
    # aflag = "!" + flagname + ";"
    # aprop = "property ", White(' ') + Word(alphanums + "_.") + "=" + SkipTo(";") + ";"
    # st << (state + Optional(st))
    # afunc = "$" + Word(alphas+"_", alphanums+"_") + Optional("(" + Optional(args) + ")") + "{" + Optional(st) + "};"
    # label = "#" + Optional("#") + Word(alphas + "_", alphanums + "_") + "{" + Optional(st) + "};"
    # possib = afunc ^ label ^ aprop ^ aflag ^ flag ^ raw
    # recurse = Forward()
    # recurse << (possib + Optional(recurse))
    # parser << ("%" + Word(alphanums + "_") + actorargs + "{" + Optional(recurse) + "};" + Optional(parser))
    # if = ('if')
    
    # comment = re.compile(r"\/\*(\*(?!\/)|[^*])*\*\/|\/\/[^\n$]+", re.MULTILINE)
    # debug = True

    # if debug:
        # args.setDebug()
        # inherit.setDebug()
        # replace.setDebug()
        # denum.setDebug()
        # actorargs.setDebug()
        # action.setDebug()
        # cond.setDebug()
        # call.setDebug()
        # raw.setDebug()
        # normstate.setDebug()
        # state.setDebug()
        # flagname.setDebug()
        # flag.setDebug()
        # aflag.setDebug()
        # aprop.setDebug()
        # st.setDebug()
        # afunc.setDebug()
        # label.setDebug()
        # possib.setDebug()
        # recurse.setDebug()
        # parser.setDebug()

    @classmethod
    def parse(cls, code):
        print("Syntax parsing...")
        data = zdlexer.parse_code(code.strip(' \t\n'))
        res = cls()

        res._parse(data)

        return res

    def _parse_literal(self, literal):
        if literal[0] == 'number':
            return str(literal[1])

        elif literal[0] == 'string':
            return literal[1]

        elif literal[0] == 'actor variable':
            return literal[1]

        elif literal[0] == 'call expr':
            return self._parse_action(literal[1])
    
    def _parse_action(self, a):
        return "{}({})".format(a[0], (', '.join(self._parse_literal(x) for x in a[1]) if a[1] is not None else []))
    
    def _parse_state_action_or_body(self, a):
        if a[0] == 'action':
            return [self._parse_state_action(a[1])]

        else:
            res = []

            for x in a[1]:
                res.extend(self._parse_state_action_or_body(x))

            return res

    def _parse_state_action(self, a):
        args = (', '.join(a[1]) if a[1] is not None else [])

        if len(args) > 0:
            return "{}({})".format(a[0], args)

        else:
            return a[0]

    def _parse_state(self, actor, label, s):
        if s[0] == 'frames':
            name, frames, duration, modifiers, action = s[1]

            for f in frames:
                if action is None:
                    label.states.append(ZDState(name, f, duration, modifiers))

                else:
                    body = self._parse_state_action_or_body(action)

                    for i, a in enumerate(body):
                        label.states.append(ZDState(name, f, (0 if i + 1 < len(body) else duration), modifiers, action=a))

        elif s[0] == 'call':
            ZDCall(self, label, s[1])

        elif s[0] == 'flow':
            label.states.append(ZDRawDecorate(s[1]))

        elif s[0] == 'repeat':
            rep = ZDRepeat(actor, s[1][0], [])

            for a in s[1][1]:
                self._parse_state(actor, rep, a)
                
            label.states.append(rep)

        elif s[0] == 'if':
            ifs = ZDIfStatement(actor, s[1][0], [])

            for a in s[1][1]:
                self._parse_state(actor, ifs, a)

            label.states.append(ifs)

        elif s[0] == 'while':
            whs = ZDWhileStatement(actor, s[1][0], [])

            for a in s[1][1]:
                self._parse_state(actor, whs, a)

            label.states.append(whs)

 
    def _parse(self, actors):
        for a in actors:
            actor = ZDActor(self, a['classname'], a['inheritance'], a['replacement'], a['class number'])

            for btype, bdata in a['body']:
                if btype == 'property':
                    ZDProperty(actor, bdata['name'], self._parse_literal(bdata['value']))

                elif btype == 'flag':
                    actor.flags.append(bdata)

                elif btype == 'flag combo':
                    actor.raw.append(bdata)

                elif btype == 'unflag':
                    actor.antiflags.append(bdata)

                elif btype == 'label':
                    label = ZDLabel(actor, bdata['name'])

                    for s in bdata['body']:
                        self._parse_state(actor, label, s)

                elif btype == 'function':
                    func = ZDFunction(self, actor, bdata['name'])

                    for s in bdata['body']:
                        self._parse_state(actor, func, s)

            self.actors.append(actor)

    def __init__(self):
        self.inventories = []
        self.actors = []
        self.calls = []

    def __decorate__(self):
        if not self.inventories:
            return "\n\n\n".join(decorate(a) for a in sorted(self.actors, key=lambda v: v.name))

        return "\n\n\n".join(["\n".join(
            decorate(i) for i in self.inventories
        )] + [
            decorate(a) for a in sorted(self.actors, key=lambda v: v.name)
        ]) # lines split for debugging

    def decorate(self):
        print("\n\nGenerating DECORATE...\n\n")
        return self.__decorate__()
