# encoding:utf-8

"""
The :mod:`parser` module concerns itself with parsing Python source.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from functools import reduce
from .. import source, diagnostic, lexer, ast

# A few notes about our approach to parsing:
#
# Python uses an LL(1) parser generator. It's a bit weird, because
# the usual reason to choose LL(1) is to make a handwritten parser
# possible, however Python's grammar is formulated in a way that
# is much more easily recognized if you make an FSM rather than
# the usual "if accept(token)..." ladder. So in a way it is
# the worst of both worlds.
#
# We don't use a parser generator because we want to have an unified
# grammar for all Python versions, and also have grammar coverage
# analysis and nice error recovery. To make the grammar compact,
# we use combinators to compose it from predefined fragments,
# such as "sequence" or "alternation" or "Kleene star". This easily
# gives us one token of lookahead in most cases, but e.g. not
# in the following one:
#
#     argument: test | test '=' test
#
# There are two issues with this. First, in an alternation, the first
# variant will be tried (and accepted) earlier. Second, if we reverse
# them, by the point it is clear ``'='`` will not be accepted, ``test``
# has already been consumed.
#
# The way we fix this is by reordering rules so that longest match
# comes first, and adding backtracking on alternations (as well as
# plus and star, since those have a hidden alternation inside).
#
# While backtracking can in principle make asymptotical complexity
# worse, it never makes parsing syntactically correct code supralinear
# with Python's LL(1) grammar, and we could not come up with any
# pathological incorrect input as well.

# Coverage data
_all_rules = []
_all_stmts = {(12480,12483): False, (12795,12798): False, (12844,12847): False, (12960,12962): False, (13126,13130): False, (13262,13266): False, (13381,13384): False, (13434,13436): False, (13589,13592): False, (13631,13633): False, (13816,13819): False, (13858,13860): False, (13902,13904): False, (14049,14053): False, (14964,14968): False, (15050,15052): False, (15148,15152): False, (15654,15656): False, (16111,16115): False, (16553,16555): False, (16645,16649): False, (16871,16874): False, (17154,17156): False, (17201,17203): False, (17256,17258): False, (17315,17317): False, (17376,17378): False, (17437,17439): False, (17953,17956): False, (18037,18039): False, (18231,18234): False, (18401,18404): False, (18467,18469): False, (18638,18642): False, (18676,18679): False, (18730,18732): False, (18914,18918): False, (19129,19133): False, (19147,19149): False, (19296,19300): False, (19483,19486): False, (19519,19521): False, (19602,19604): False, (19846,19849): False, (19977,19979): False, (20155,20158): False, (20312,20314): False, (20489,20492): False, (20847,20850): False, (21101,21104): False, (21450,21452): False, (21763,21766): False, (22200,22203): False, (22853,22856): False, (23050,23052): False, (23883,23886): False, (24187,24190): False, (24373,24375): False, (24694,24697): False, (24995,24998): False, (25267,25270): False, (25315,25317): False, (25491,25495): False, (25831,25834): False, (25880,25882): False, (26010,26014): False, (26059,26061): False, (26166,26170): False, (26303,26306): False, (26697,26700): False, (26867,26870): False, (27241,27244): False, (27445,27447): False, (27684,27687): False, (27736,27738): False, (27924,27928): False, (28029,28031): False, (28114,28118): False, (28573,28576): False, (28641,28643): False, (28888,28892): False, (29164,29167): False, (29218,29221): False, (29270,29272): False, (29462,29466): False, (29826,29829): False, (29879,29881): False, (30021,30025): False, (30078,30080): False, (30193,30197): False, (31656,31659): False, (31754,31756): False, (32033,32036): False, (33206,33209): False, (33393,33396): False, (33429,33431): False, (33617,33621): False, (33721,33724): False, (34092,34094): False, (34139,34141): False, (34435,34439): False, (34588,34592): False, (34766,34770): False, (35625,35628): False, (35704,35706): False, (35989,35992): False, (36095,36097): False, (36311,36314): False, (36529,36532): False, (36778,36780): False, (36840,36844): False, (36988,36991): False, (37404,37407): False, (37791,37794): False, (37952,37955): False, (38151,38154): False, (38270,38272): False, (38454,38457): False, (38785,38788): False, (38974,38976): False, (39076,39078): False, (39188,39190): False, (39485,39488): False, (39663,39665): False, (39760,39762): False, (40182,40185): False, (40428,40431): False, (40509,40512): False, (40645,40648): False, (40736,40738): False, (40972,40975): False, (41179,41182): False, (41446,41449): False, (41772,41775): False, (42386,42388): False, (42552,42554): False, (42615,42617): False, (43074,43077): False, (43254,43256): False, (43664,43667): False, (43913,43915): False, (44587,44590): False, (44855,44858): False, (45338,45341): False, (45551,45553): False, (45619,45621): False, (45685,45689): False, (45952,45955): False, (46387,46390): False, (46533,46535): False, (46882,46885): False, (47293,47296): False, (47550,47552): False, (47643,47646): False, (47827,47829): False, (48192,48194): False, (48425,48428): False, (48832,48834): False, (49181,49184): False, (49644,49646): False, (50019,50022): False, (50103,50106): False, (50388,50390): False, (50566,50568): False, (51048,51051): False, (51470,51473): False, (52017,52020): False, (52167,52169): False, (52404,52408): False, (52927,52930): False, (53311,53314): False, (53411,53413): False, (53644,53648): False, (53848,53851): False, (53974,53977): False, (54184,54187): False, (54463,54465): False, (54563,54565): False, (54647,54649): False, (54762,54766): False, (55116,55119): False, (55768,55771): False, (55912,55914): False, (56386,56389): False, (56426,56428): False, (56906,56909): False, (56979,56981): False, (57738,57741): False, (57824,57826): False, (58103,58107): False, (58213,58216): False, (58302,58304): False, (58582,58586): False, (58673,58676): False, (59172,59175): False, (59398,59400): False, (59640,59644): False, (59720,59723): False, (59816,59818): False, (60027,60030): False, (61728,61731): False, (62052,62055): False, (62154,62157): False, (62191,62193): False, (62317,62321): False, (62477,62479): False, (62726,62729): False, (62827,62830): False, (62988,62991): False, (63130,63133): False, (63379,63382): False, (63433,63435): False, (63463,63466): False, (64861,64864): False, (64983,64986): False, (65014,65016): False, (65070,65074): False, (65128,65132): False, (66089,66092): False, (66134,66136): False, (66187,66191): False, (66320,66324): False, (66477,66480): False, (66643,66646): False, (67047,67050): False, (67232,67235): False, (67273,67275): False, (67348,67352): False, (67822,67825): False, (68009,68012): False, (68373,68376): False, (68941,68944): False, (69048,69050): False, (69155,69159): False, (69592,69596): False, (69856,69859): False, (70063,70066): False, (70161,70163): False, (70225,70227): False, (70326,70328): False, (70438,70440): False, (70681,70684): False, (71345,71348): False, (71678,71681): False, (71877,71880): False, (72428,72431): False, (72477,72479): False, (72795,72799): False, (73158,73161): False, (73207,73209): False, (73329,73333): False, (73877,73880): False, (74092,74094): False, (74806,74809): False, (75124,75126): False, (76062,76065): False, (76164,76166): False, (76231,76234): False, (76268,76270): False, (76780,76783): False, (77287,77290): False, (77327,77329): False, (77400,77404): False, (77585,77588): False, (77809,77812): False, (77838,77840): False, (77925,77929): False, (78191,78195): False, (78301,78304): False, (78348,78351): False, (78376,78378): False, (78830,78833): False, (78873,78876): False, (78901,78903): False, (79291,79294): False, (79697,79700): False, (79778,79781): False, (80032,80034): False, (80105,80109): False, (80177,80180): False, (80240,80243): False, (80458,80460): False, (80531,80535): False, (82068,82071): False, (82191,82193): False, (82344,82348): False, (82516,82519): False, (82619,82621): False, (82773,82777): False, (82922,82926): False, (83083,83086): False}

# Generic LL parsing combinators
class Unmatched:
    pass

unmatched = Unmatched()

def llrule(loc, expected, cases=1):
    if loc is None:
        def decorator(rule):
            rule.expected = expected
            return rule
    else:
        def decorator(inner_rule):
            if cases == 1:
                def rule(*args, **kwargs):
                    result = inner_rule(*args, **kwargs)
                    if result is not unmatched:
                        rule.covered[0] = True
                    return result
            else:
                rule = inner_rule

            rule.loc, rule.expected, rule.covered = \
                loc, expected, [False] * cases
            _all_rules.append(rule)

            return rule
    return decorator

def action(inner_rule, loc=None):
    """
    A decorator returning a function that first runs ``inner_rule`` and then, if its
    return value is not None, maps that value using ``mapper``.

    If the value being mapped is a tuple, it is expanded into multiple arguments.

    Similar to attaching semantic actions to rules in traditional parser generators.
    """
    def decorator(mapper):
        @llrule(loc, inner_rule.expected)
        def outer_rule(parser):
            result = inner_rule(parser)
            if result is unmatched:
                return result
            if isinstance(result, tuple):
                return mapper(parser, *result)
            else:
                return mapper(parser, result)
        return outer_rule
    return decorator

def Eps(value=None, loc=None):
    """A rule that accepts no tokens (epsilon) and returns ``value``."""
    @llrule(loc, lambda parser: [])
    def rule(parser):
        return value
    return rule

def Tok(kind, loc=None):
    """A rule that accepts a token of kind ``kind`` and returns it, or returns None."""
    @llrule(loc, lambda parser: [kind])
    def rule(parser):
        return parser._accept(kind)
    return rule

def Loc(kind, loc=None):
    """A rule that accepts a token of kind ``kind`` and returns its location, or returns None."""
    @llrule(loc, lambda parser: [kind])
    def rule(parser):
        result = parser._accept(kind)
        if result is unmatched:
            return result
        return result.loc
    return rule

def Rule(name, loc=None):
    """A proxy for a rule called ``name`` which may not be yet defined."""
    @llrule(loc, lambda parser: getattr(parser, name).expected(parser))
    def rule(parser):
        return getattr(parser, name)()
    return rule

def Expect(inner_rule, loc=None):
    """A rule that executes ``inner_rule`` and emits a diagnostic error if it returns None."""
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            expected = reduce(list.__add__, [rule.expected(parser) for rule in parser._errrules])
            expected = list(sorted(set(expected)))

            if len(expected) > 1:
                expected = " or ".join([", ".join(expected[0:-1]), expected[-1]])
            elif len(expected) == 1:
                expected = expected[0]
            else:
                expected = "(impossible)"

            error_tok = parser._tokens[parser._errindex]
            error = diagnostic.Diagnostic(
                "fatal", "unexpected {actual}: expected {expected}",
                {"actual": error_tok.kind, "expected": expected},
                error_tok.loc)
            parser.diagnostic_engine.process(error)
        return result
    return rule

def Seq(first_rule, *rest_of_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns a tuple
    containing their return values, or None if the first rule was not satisfied.
    """
    @llrule(kwargs.get("loc", None), first_rule.expected)
    def rule(parser):
        result = first_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        for rule in rest_of_rules:
            result = rule(parser)
            if result is unmatched:
                return result
            results.append(result)
        return tuple(results)
    return rule

def SeqN(n, *inner_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns
    the value returned by rule number ``n``, or None if the first rule was not satisfied.
    """
    @action(Seq(*inner_rules), loc=kwargs.get("loc", None))
    def rule(parser, *values):
        return values[n]
    return rule

def Alt(*inner_rules, **kwargs):
    """
    A rule that expects a sequence of tokens satisfying one of ``rules`` in sequence
    (a rule is satisfied when it returns anything but None) and returns the return
    value of that rule, or None if no rules were satisfied.
    """
    loc = kwargs.get("loc", None)
    expected = lambda parser: reduce(list.__add__, map(lambda x: x.expected(parser), inner_rules))
    if loc is not None:
        @llrule(loc, expected, cases=len(inner_rules))
        def rule(parser):
            data = parser._save()
            for idx, inner_rule in enumerate(inner_rules):
                result = inner_rule(parser)
                if result is unmatched:
                    parser._restore(data, rule=inner_rule)
                else:
                    rule.covered[idx] = True
                    return result
            return unmatched
    else:
        @llrule(loc, expected, cases=len(inner_rules))
        def rule(parser):
            data = parser._save()
            for inner_rule in inner_rules:
                result = inner_rule(parser)
                if result is unmatched:
                    parser._restore(data, rule=inner_rule)
                else:
                    return result
            return unmatched
    return rule

def Opt(inner_rule, loc=None):
    """Shorthand for ``Alt(inner_rule, Eps())``"""
    return Alt(inner_rule, Eps(), loc=loc)

def Star(inner_rule, loc=None):
    """
    A rule that accepts a sequence of tokens satisfying ``inner_rule`` zero or more times,
    and returns the returned values in a :class:`list`.
    """
    @llrule(loc, lambda parser: [])
    def rule(parser):
        results = []
        while True:
            data = parser._save()
            result = inner_rule(parser)
            if result is unmatched:
                parser._restore(data, rule=inner_rule)
                return results
            results.append(result)
    return rule

def Plus(inner_rule, loc=None):
    """
    A rule that accepts a sequence of tokens satisfying ``inner_rule`` one or more times,
    and returns the returned values in a :class:`list`.
    """
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        while True:
            data = parser._save()
            result = inner_rule(parser)
            if result is unmatched:
                parser._restore(data, rule=inner_rule)
                return results
            results.append(result)
    return rule

class commalist(list):
    __slots__ = ("trailing_comma",)

def List(inner_rule, separator_tok, trailing, leading=True, loc=None):
    if not trailing:
        @action(Seq(inner_rule, Star(SeqN(1, Tok(separator_tok), inner_rule))), loc=loc)
        def outer_rule(parser, first, rest):
            return [first] + rest
        return outer_rule
    else:
        # A rule like this: stmt (';' stmt)* [';']
        # This doesn't yield itself to combinators above, because disambiguating
        # another iteration of the Kleene star and the trailing separator
        # requires two lookahead tokens (naively).
        separator_rule = Tok(separator_tok)
        @llrule(loc, inner_rule.expected)
        def rule(parser):
            results = commalist()

            if leading:
                result = inner_rule(parser)
                if result is unmatched:
                    return result
                else:
                    results.append(result)

            while True:
                result = separator_rule(parser)
                if result is unmatched:
                    results.trailing_comma = None
                    return results

                result_1 = inner_rule(parser)
                if result_1 is unmatched:
                    results.trailing_comma = result
                    return results
                else:
                    results.append(result_1)
        return rule

# Python AST specific parser combinators
def Newline(loc=None):
    """A rule that accepts token of kind ``newline`` and returns an empty list."""
    @llrule(loc, lambda parser: ["newline"])
    def rule(parser):
        result = parser._accept("newline")
        if result is unmatched:
            return result
        return []
    return rule

def Oper(klass, *kinds, **kwargs):
    """
    A rule that accepts a sequence of tokens of kinds ``kinds`` and returns
    an instance of ``klass`` with ``loc`` encompassing the entire sequence
    or None if the first token is not of ``kinds[0]``.
    """
    @action(Seq(*map(Loc, kinds)), loc=kwargs.get("loc", None))
    def rule(parser, *tokens):
        return klass(loc=tokens[0].join(tokens[-1]))
    return rule

def BinOper(expr_rulename, op_rule, node=ast.BinOp, loc=None):
    @action(Seq(Rule(expr_rulename), Star(Seq(op_rule, Rule(expr_rulename)))), loc=loc)
    def rule(parser, lhs, trailers):
        for (op, rhs) in trailers:
            lhs = node(left=lhs, op=op, right=rhs,
                       loc=lhs.loc.join(rhs.loc))
        return lhs
    return rule

def BeginEnd(begin_tok, inner_rule, end_tok, empty=None, loc=None):
    @action(Seq(Loc(begin_tok), inner_rule, Loc(end_tok)), loc=loc)
    def rule(parser, begin_loc, node, end_loc):
        if node is None:
            node = empty(parser)

        # Collection nodes don't have loc yet. If a node has loc at this
        # point, it means it's an expression passed in parentheses.
        if node.loc is None and type(node) in [
                ast.List, ast.ListComp,
                ast.Dict, ast.DictComp,
                ast.Set, ast.SetComp,
                ast.GeneratorExp,
                ast.Tuple, ast.Repr,
                ast.Call, ast.Subscript,
                ast.arguments]:
            node.begin_loc, node.end_loc, node.loc = \
                begin_loc, end_loc, begin_loc.join(end_loc)
        return node
    return rule

class Parser:

    # Generic LL parsing methods
    def __init__(self, lexer, version, diagnostic_engine):
        _all_stmts[(12480,12483)] = True
        self._init_version(version)
        self.diagnostic_engine = diagnostic_engine

        self.lexer     = lexer
        self._tokens   = []
        self._index    = -1
        self._errindex = -1
        self._errrules = []
        self._advance()

    def _save(self):
        _all_stmts[(12795,12798)] = True
        return self._index

    def _restore(self, data, rule):
        _all_stmts[(12844,12847)] = True
        self._index = data
        self._token = self._tokens[self._index]

        if self._index > self._errindex:
            # We have advanced since last error
            _all_stmts[(12960,12962)] = True
            self._errindex = self._index
            self._errrules = [rule]
        elif self._index == self._errindex:
            # We're at the same place as last error
            _all_stmts[(13126,13130)] = True
            self._errrules.append(rule)
        else:
            # We've backtracked far and are now just failing the
            # whole parse
            _all_stmts[(13262,13266)] = True
            pass

    def _advance(self):
        _all_stmts[(13381,13384)] = True
        self._index += 1
        if self._index == len(self._tokens):
            _all_stmts[(13434,13436)] = True
            self._tokens.append(self.lexer.next(eof_token=True))
        self._token = self._tokens[self._index]

    def _accept(self, expected_kind):
        _all_stmts[(13589,13592)] = True
        if self._token.kind == expected_kind:
            _all_stmts[(13631,13633)] = True
            result = self._token
            self._advance()
            return result
        return unmatched

    # Python-specific methods
    def _init_version(self, version):
        _all_stmts[(13816,13819)] = True
        if version in ((2, 6), (2, 7)):
            _all_stmts[(13858,13860)] = True
            if version == (2, 6):
                _all_stmts[(13902,13904)] = True
                self.with_stmt       = self.with_stmt__26
                self.atom_6          = self.atom_6__26
            else:
                _all_stmts[(14049,14053)] = True
                self.with_stmt       = self.with_stmt__27
                self.atom_6          = self.atom_6__27
            self.except_clause_1 = self.except_clause_1__26
            self.classdef        = self.classdef__26
            self.subscript       = self.subscript__26
            self.raise_stmt      = self.raise_stmt__26
            self.comp_if         = self.comp_if__26
            self.atom            = self.atom__26
            self.funcdef         = self.funcdef__26
            self.parameters      = self.parameters__26
            self.varargslist     = self.varargslist__26
            self.comparison_1    = self.comparison_1__26
            self.exprlist_1      = self.exprlist_1__26
            self.testlist_comp_1 = self.testlist_comp_1__26
            self.expr_stmt_1     = self.expr_stmt_1__26
            self.yield_expr      = self.yield_expr__26
            return
        elif version in ((3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)):
            _all_stmts[(14964,14968)] = True
            if version == (3, 0):
                _all_stmts[(15050,15052)] = True
                self.with_stmt       = self.with_stmt__26 # lol
            else:
                _all_stmts[(15148,15152)] = True
                self.with_stmt       = self.with_stmt__27
            self.except_clause_1 = self.except_clause_1__30
            self.classdef        = self.classdef__30
            self.subscript       = self.subscript__30
            self.raise_stmt      = self.raise_stmt__30
            self.comp_if         = self.comp_if__30
            self.atom            = self.atom__30
            self.funcdef         = self.funcdef__30
            self.parameters      = self.parameters__30
            if version < (3, 2):
                _all_stmts[(15654,15656)] = True
                self.varargslist     = self.varargslist__30
                self.typedargslist   = self.typedargslist__30
                self.comparison_1    = self.comparison_1__30
                self.star_expr       = self.star_expr__30
                self.exprlist_1      = self.exprlist_1__30
                self.testlist_comp_1 = self.testlist_comp_1__26
                self.expr_stmt_1     = self.expr_stmt_1__26
            else:
                _all_stmts[(16111,16115)] = True
                self.varargslist     = self.varargslist__32
                self.typedargslist   = self.typedargslist__32
                self.comparison_1    = self.comparison_1__32
                self.star_expr       = self.star_expr__32
                self.exprlist_1      = self.exprlist_1__32
                self.testlist_comp_1 = self.testlist_comp_1__32
                self.expr_stmt_1     = self.expr_stmt_1__32
            if version < (3, 3):
                _all_stmts[(16553,16555)] = True
                self.yield_expr      = self.yield_expr__26
            else:
                _all_stmts[(16645,16649)] = True
                self.yield_expr      = self.yield_expr__33
            return

        raise NotImplementedError("pythonparser.parser.Parser cannot parse Python %s" %
                                  str(version))

    def _arguments(self, args=None, defaults=None, kwonlyargs=None, kw_defaults=None,
                   vararg=None, kwarg=None,
                   star_loc=None, dstar_loc=None, begin_loc=None, end_loc=None,
                   equals_locs=None, kw_equals_locs=None, loc=None):
        _all_stmts[(16871,16874)] = True
        if args is None:
            _all_stmts[(17154,17156)] = True
            args = []
        if defaults is None:
            _all_stmts[(17201,17203)] = True
            defaults = []
        if kwonlyargs is None:
            _all_stmts[(17256,17258)] = True
            kwonlyargs = []
        if kw_defaults is None:
            _all_stmts[(17315,17317)] = True
            kw_defaults = []
        if equals_locs is None:
            _all_stmts[(17376,17378)] = True
            equals_locs = []
        if kw_equals_locs is None:
            _all_stmts[(17437,17439)] = True
            kw_equals_locs = []
        return ast.arguments(args=args, defaults=defaults,
                             kwonlyargs=kwonlyargs, kw_defaults=kw_defaults,
                             vararg=vararg, kwarg=kwarg,
                             star_loc=star_loc, dstar_loc=dstar_loc,
                             begin_loc=begin_loc, end_loc=end_loc,
                             equals_locs=equals_locs, kw_equals_locs=kw_equals_locs,
                             loc=loc)

    def _arg(self, tok, colon_loc=None, annotation=None):
        _all_stmts[(17953,17956)] = True
        loc = tok.loc
        if annotation:
            _all_stmts[(18037,18039)] = True
            loc = loc.join(annotation.loc)
        return ast.arg(arg=tok.value, annotation=annotation,
                       arg_loc=tok.loc, colon_loc=colon_loc, loc=loc)

    def _empty_arglist(self):
        _all_stmts[(18231,18234)] = True
        return ast.Call(args=[], keywords=[], starargs=None, kwargs=None,
                        star_loc=None, dstar_loc=None, loc=None)

    def _wrap_tuple(self, elts):
        _all_stmts[(18401,18404)] = True
        assert len(elts) > 0
        if len(elts) > 1:
            _all_stmts[(18467,18469)] = True
            return ast.Tuple(ctx=None, elts=elts,
                             loc=elts[0].loc.join(elts[-1].loc), begin_loc=None, end_loc=None)
        else:
            _all_stmts[(18638,18642)] = True
            return elts[0]

    def _assignable(self, node, is_delete=False):
        _all_stmts[(18676,18679)] = True
        if isinstance(node, ast.Name) or isinstance(node, ast.Subscript) or \
                isinstance(node, ast.Attribute) or isinstance(node, ast.Starred):
            _all_stmts[(18730,18732)] = True
            return node
        elif (isinstance(node, ast.List) or isinstance(node, ast.Tuple)) and \
                any(node.elts):
            _all_stmts[(18914,18918)] = True
            node.elts = [self._assignable(elt, is_delete) for elt in node.elts]
            return node
        else:
            _all_stmts[(19129,19133)] = True
            if is_delete:
                _all_stmts[(19147,19149)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "cannot delete this expression", {}, node.loc)
            else:
                _all_stmts[(19296,19300)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "cannot assign to this expression", {}, node.loc)
            self.diagnostic_engine.process(error)

    def add_flags(self, flags):
        _all_stmts[(19483,19486)] = True
        if "print_function" in flags:
            _all_stmts[(19519,19521)] = True
            self.lexer.print_function = True
        if "unicode_literals" in flags:
            _all_stmts[(19602,19604)] = True
            self.lexer.unicode_literals = True

    # Grammar
    @action(Expect(Alt(Newline(loc=(19719,19726)),
                       Rule("simple_stmt", loc=(19753,19757)),
                       SeqN(0, Rule("compound_stmt", loc=(19805,19809)), Newline(loc=(19828,19835)), loc=(19797,19801)), loc=(19715,19718)), loc=(19708,19714)), loc=(19701,19707))
    def single_input(self, body):
        _all_stmts[(19846,19849)] = True
        """single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE"""
        loc = None
        if body != []:
            _all_stmts[(19977,19979)] = True
            loc = body[0].loc
        return ast.Interactive(body=body, loc=loc)

    @action(Expect(SeqN(0, Star(Alt(Newline(loc=(20110,20117)), Rule("stmt", loc=(20121,20125)), loc=(20106,20109)), loc=(20101,20105)), Tok("eof", loc=(20137,20140)), loc=(20093,20097)), loc=(20086,20092)), loc=(20079,20085))
    def file_input(parser, body):
        _all_stmts[(20155,20158)] = True
        """file_input: (NEWLINE | stmt)* ENDMARKER"""
        body = reduce(list.__add__, body, [])
        loc = None
        if body != []:
            _all_stmts[(20312,20314)] = True
            loc = body[0].loc
        return ast.Module(body=body, loc=loc)

    @action(Expect(SeqN(0, Rule("testlist", loc=(20431,20435)), Star(Tok("newline", loc=(20454,20457)), loc=(20449,20453)), Tok("eof", loc=(20471,20474)), loc=(20423,20427)), loc=(20416,20422)), loc=(20409,20415))
    def eval_input(self, expr):
        _all_stmts[(20489,20492)] = True
        """eval_input: testlist NEWLINE* ENDMARKER"""
        return ast.Expression(body=[expr], loc=expr.loc)

    @action(Seq(Loc("@", loc=(20645,20648)), List(Tok("ident", loc=(20660,20663)), ".", trailing=False, loc=(20655,20659)),
                Opt(BeginEnd("(", Opt(Rule("arglist", loc=(20734,20738)), loc=(20730,20733)), ")",
                             empty=_empty_arglist, loc=(20716,20724)), loc=(20712,20715)),
                Loc("newline", loc=(20826,20829)), loc=(20641,20644)), loc=(20634,20640))
    def decorator(self, at_loc, idents, call_opt, newline_loc):
        _all_stmts[(20847,20850)] = True
        """decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE"""
        root = idents[0]
        dec_loc = root.loc
        expr = ast.Name(id=root.value, ctx=None, loc=root.loc)
        for ident in idents[1:]:
          _all_stmts[(21101,21104)] = True
          dot_loc = ident.loc.begin()
          dot_loc.begin_pos -= 1
          dec_loc = dec_loc.join(ident.loc)
          expr = ast.Attribute(value=expr, attr=ident.value, ctx=None,
                               loc=expr.loc.join(ident.loc),
                               attr_loc=ident.loc, dot_loc=dot_loc)

        if call_opt:
            _all_stmts[(21450,21452)] = True
            call_opt.func = expr
            call_opt.loc = dec_loc.join(call_opt.loc)
            expr = call_opt
        return at_loc, expr

    decorators = Plus(Rule("decorator", loc=(21629,21633)), loc=(21624,21628))
    """decorators: decorator+"""

    @action(Seq(Rule("decorators", loc=(21698,21702)), Alt(Rule("classdef", loc=(21722,21726)), Rule("funcdef", loc=(21740,21744)), loc=(21718,21721)), loc=(21694,21697)), loc=(21687,21693))
    def decorated(self, decorators, classfuncdef):
        _all_stmts[(21763,21766)] = True
        """decorated: decorators (classdef | funcdef)"""
        classfuncdef.at_locs = list(map(lambda x: x[0], decorators))
        classfuncdef.decorator_list = list(map(lambda x: x[1], decorators))
        classfuncdef.loc = classfuncdef.loc.join(decorators[0][0])
        return classfuncdef

    @action(Seq(Loc("def", loc=(22124,22127)), Tok("ident", loc=(22136,22139)), Rule("parameters", loc=(22150,22154)), Loc(":", loc=(22170,22173)), Rule("suite", loc=(22180,22184)), loc=(22120,22123)), loc=(22113,22119))
    def funcdef__26(self, def_loc, ident_tok, args, colon_loc, suite):
        _all_stmts[(22200,22203)] = True
        """(2.6, 2.7) funcdef: 'def' NAME parameters ':' suite"""
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=None,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=None,
                               loc=def_loc.join(suite[-1].loc))

    @action(Seq(Loc("def", loc=(22710,22713)), Tok("ident", loc=(22722,22725)), Rule("parameters", loc=(22736,22740)),
                Opt(Seq(Loc("->", loc=(22780,22783)), Rule("test", loc=(22791,22795)), loc=(22776,22779)), loc=(22772,22775)),
                Loc(":", loc=(22823,22826)), Rule("suite", loc=(22833,22837)), loc=(22706,22709)), loc=(22699,22705))
    def funcdef__30(self, def_loc, ident_tok, args, returns_opt, colon_loc, suite):
        _all_stmts[(22853,22856)] = True
        """(3.0-) funcdef: 'def' NAME parameters ['->' test] ':' suite"""
        arrow_loc = returns = None
        if returns_opt:
            _all_stmts[(23050,23052)] = True
            arrow_loc, returns = returns_opt
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=returns,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=arrow_loc,
                               loc=def_loc.join(suite[-1].loc))

    parameters__26 = BeginEnd("(", Opt(Rule("varargslist", loc=(23519,23523)), loc=(23515,23518)), ")", empty=_arguments, loc=(23501,23509))
    """(2.6, 2.7) parameters: '(' [varargslist] ')'"""

    parameters__30 = BeginEnd("(", Opt(Rule("typedargslist", loc=(23659,23663)), loc=(23655,23658)), ")", empty=_arguments, loc=(23641,23649))
    """(3.0) parameters: '(' [typedargslist] ')'"""

    varargslist__26_1 = Seq(Rule("fpdef", loc=(23787,23791)), Opt(Seq(Loc("=", loc=(23810,23813)), Rule("test", loc=(23820,23824)), loc=(23806,23809)), loc=(23802,23805)), loc=(23783,23786))

    @action(Seq(Loc("**", loc=(23853,23856)), Tok("ident", loc=(23864,23867)), loc=(23849,23852)), loc=(23842,23848))
    def varargslist__26_2(self, dstar_loc, kwarg_tok):
        _all_stmts[(23883,23886)] = True
        return self._arguments(kwarg=self._arg(kwarg_tok),
                               dstar_loc=dstar_loc, loc=dstar_loc.join(kwarg_tok.loc))

    @action(Seq(Loc("*", loc=(24097,24100)), Tok("ident", loc=(24107,24110)),
                Opt(Seq(Tok(",", loc=(24145,24148)), Loc("**", loc=(24155,24158)), Tok("ident", loc=(24166,24169)), loc=(24141,24144)), loc=(24137,24140)), loc=(24093,24096)), loc=(24086,24092))
    def varargslist__26_3(self, star_loc, vararg_tok, kwarg_opt):
        _all_stmts[(24187,24190)] = True
        dstar_loc = kwarg = None
        loc = star_loc.join(vararg_tok.loc)
        vararg = self._arg(vararg_tok)
        if kwarg_opt:
            _all_stmts[(24373,24375)] = True
            _, dstar_loc, kwarg_tok = kwarg_opt
            kwarg = self._arg(kwarg_tok)
            loc = star_loc.join(kwarg_tok.loc)
        return self._arguments(vararg=vararg, kwarg=kwarg,
                               star_loc=star_loc, dstar_loc=dstar_loc, loc=loc)

    @action(Eps(value=(), loc=(24675,24678)), loc=(24668,24674))
    def varargslist__26_4(self):
        _all_stmts[(24694,24697)] = True
        return self._arguments()

    @action(Alt(Seq(Star(SeqN(0, varargslist__26_1, Tok(",", loc=(24809,24812)), loc=(24782,24786)), loc=(24777,24781)),
                    Alt(varargslist__26_2, varargslist__26_3, loc=(24841,24844)), loc=(24773,24776)),
                Seq(List(varargslist__26_1, ",", trailing=True, loc=(24905,24909)),
                    varargslist__26_4, loc=(24901,24904)), loc=(24769,24772)), loc=(24762,24768))
    def varargslist__26(self, fparams, args):
        _all_stmts[(24995,24998)] = True
        """
        (2.6, 2.7)
        varargslist: ((fpdef ['=' test] ',')*
                      ('*' NAME [',' '**' NAME] | '**' NAME) |
                      fpdef ['=' test] (',' fpdef ['=' test])* [','])
        """
        for fparam, default_opt in fparams:
            _all_stmts[(25267,25270)] = True
            if default_opt:
                _all_stmts[(25315,25317)] = True
                equals_loc, default = default_opt
                args.equals_locs.append(equals_loc)
                args.defaults.append(default)
            elif len(args.defaults) > 0:
                _all_stmts[(25491,25495)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "non-default argument follows default argument", {},
                    fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                self.diagnostic_engine.process(error)

            args.args.append(fparam)

        def fparam_loc(fparam, default_opt):
            _all_stmts[(25831,25834)] = True
            if default_opt:
                _all_stmts[(25880,25882)] = True
                equals_loc, default = default_opt
                return fparam.loc.join(default.loc)
            else:
                _all_stmts[(26010,26014)] = True
                return fparam.loc

        if args.loc is None:
            _all_stmts[(26059,26061)] = True
            args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
        elif len(fparams) > 0:
            _all_stmts[(26166,26170)] = True
            args.loc = args.loc.join(fparam_loc(*fparams[0]))

        return args

    @action(Tok("ident", loc=(26285,26288)), loc=(26278,26284))
    def fpdef_1(self, ident_tok):
        _all_stmts[(26303,26306)] = True
        return ast.arg(arg=ident_tok.value, annotation=None,
                       arg_loc=ident_tok.loc, colon_loc=None,
                       loc=ident_tok.loc)

    fpdef = Alt(fpdef_1, BeginEnd("(", Rule("fplist", loc=(26538,26542)), ")",
                                  empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(26524,26532)), loc=(26511,26514))
    """fpdef: NAME | '(' fplist ')'"""

    def _argslist(fpdef_rule, old_style=False):
        _all_stmts[(26697,26700)] = True
        argslist_1 = Seq(fpdef_rule, Opt(Seq(Loc("=", loc=(26786,26789)), Rule("test", loc=(26796,26800)), loc=(26782,26785)), loc=(26778,26781)), loc=(26762,26765))

        @action(Seq(Loc("**", loc=(26833,26836)), Tok("ident", loc=(26844,26847)), loc=(26829,26832)), loc=(26822,26828))
        def argslist_2(self, dstar_loc, kwarg_tok):
            _all_stmts[(26867,26870)] = True
            return self._arguments(kwarg=self._arg(kwarg_tok),
                                   dstar_loc=dstar_loc, loc=dstar_loc.join(kwarg_tok.loc))

        @action(Seq(Loc("*", loc=(27086,27089)), Tok("ident", loc=(27096,27099)),
                    Star(SeqN(1, Tok(",", loc=(27143,27146)), argslist_1, loc=(27135,27139)), loc=(27130,27134)),
                    Opt(Seq(Tok(",", loc=(27195,27198)), Loc("**", loc=(27205,27208)), Tok("ident", loc=(27216,27219)), loc=(27191,27194)), loc=(27187,27190)), loc=(27082,27085)), loc=(27075,27081))
        def argslist_3(self, star_loc, vararg_tok, fparams, kwarg_opt):
            _all_stmts[(27241,27244)] = True
            dstar_loc = kwarg = None
            loc = star_loc.join(vararg_tok.loc)
            vararg = self._arg(vararg_tok)
            if kwarg_opt:
                _all_stmts[(27445,27447)] = True
                _, dstar_loc, kwarg_tok = kwarg_opt
                kwarg = self._arg(kwarg_tok)
                loc = star_loc.join(kwarg_tok.loc)
            kwonlyargs, kw_defaults, kw_equals_locs = [], [], []
            for fparam, default_opt in fparams:
                _all_stmts[(27684,27687)] = True
                if default_opt:
                    _all_stmts[(27736,27738)] = True
                    equals_loc, default = default_opt
                    kw_equals_locs.append(equals_loc)
                    kw_defaults.append(default)
                else:
                    _all_stmts[(27924,27928)] = True
                    kw_defaults.append(None)
                kwonlyargs.append(fparam)
            if any(kw_defaults):
                _all_stmts[(28029,28031)] = True
                loc = loc.join(kw_defaults[-1].loc)
            elif any(kwonlyargs):
                _all_stmts[(28114,28118)] = True
                loc = loc.join(kwonlyargs[-1].loc)
            return self._arguments(vararg=vararg, kwarg=kwarg,
                                   kwonlyargs=kwonlyargs, kw_defaults=kw_defaults,
                                   star_loc=star_loc, dstar_loc=dstar_loc,
                                   kw_equals_locs=kw_equals_locs, loc=loc)

        argslist_4 = Alt(argslist_2, argslist_3, loc=(28505,28508))

        @action(Eps(value=(), loc=(28550,28553)), loc=(28543,28549))
        def argslist_5(self):
            _all_stmts[(28573,28576)] = True
            return self._arguments()

        if old_style:
            _all_stmts[(28641,28643)] = True
            argslist = Alt(Seq(Star(SeqN(0, argslist_1, Tok(",", loc=(28711,28714)), loc=(28691,28695)), loc=(28686,28690)),
                               argslist_4, loc=(28682,28685)),
                           Seq(List(argslist_1, ",", trailing=True, loc=(28798,28802)),
                               argslist_5, loc=(28794,28797)), loc=(28678,28681))
        else:
            _all_stmts[(28888,28892)] = True
            argslist = Alt(Seq(Eps(value=[], loc=(28925,28928)), argslist_4, loc=(28921,28924)),
                           Seq(List(argslist_1, ",", trailing=False, loc=(28984,28988)),
                               Alt(SeqN(1, Tok(",", loc=(29066,29069)), Alt(argslist_4, argslist_5, loc=(29076,29079)), loc=(29058,29062)),
                                   argslist_5, loc=(29054,29057)), loc=(28980,28983)), loc=(28917,28920))

        def argslist_action(self, fparams, args):
            _all_stmts[(29164,29167)] = True
            for fparam, default_opt in fparams:
                _all_stmts[(29218,29221)] = True
                if default_opt:
                    _all_stmts[(29270,29272)] = True
                    equals_loc, default = default_opt
                    args.equals_locs.append(equals_loc)
                    args.defaults.append(default)
                elif len(args.defaults) > 0:
                    _all_stmts[(29462,29466)] = True
                    error = diagnostic.Diagnostic(
                        "fatal", "non-default argument follows default argument", {},
                        fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                    self.diagnostic_engine.process(error)

                args.args.append(fparam)

            def fparam_loc(fparam, default_opt):
                _all_stmts[(29826,29829)] = True
                if default_opt:
                    _all_stmts[(29879,29881)] = True
                    equals_loc, default = default_opt
                    return fparam.loc.join(default.loc)
                else:
                    _all_stmts[(30021,30025)] = True
                    return fparam.loc

            if args.loc is None:
                _all_stmts[(30078,30080)] = True
                args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
            elif len(fparams) > 0:
                _all_stmts[(30193,30197)] = True
                args.loc = args.loc.join(fparam_loc(*fparams[0]))

            return args

        return action(argslist, loc=(30323,30329))(argslist_action)

    typedargslist__30 = _argslist(Rule("tfpdef", loc=(30392,30396)), old_style=True)
    """
    (3.0, 3.1)
    typedargslist: ((tfpdef ['=' test] ',')*
                    ('*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
                    | tfpdef ['=' test] (',' tfpdef ['=' test])* [','])
    """

    typedargslist__32 = _argslist(Rule("tfpdef", loc=(30699,30703)))
    """
    (3.2-)
    typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [','
           ['*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef]]
         |  '*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
    """

    varargslist__30 = _argslist(Rule("vfpdef", loc=(31010,31014)), old_style=True)
    """
    (3.0, 3.1)
    varargslist: ((vfpdef ['=' test] ',')*
                  ('*' [vfpdef] (',' vfpdef ['=' test])*  [',' '**' vfpdef] | '**' vfpdef)
                  | vfpdef ['=' test] (',' vfpdef ['=' test])* [','])
    """

    varargslist__32 = _argslist(Rule("vfpdef", loc=(31310,31314)))
    """
    (3.2-)
    varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [','
           ['*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef]]
         |  '*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef)
    """

    @action(Seq(Tok("ident", loc=(31603,31606)), Opt(Seq(Loc(":", loc=(31625,31628)), Rule("test", loc=(31635,31639)), loc=(31621,31624)), loc=(31617,31620)), loc=(31599,31602)), loc=(31592,31598))
    def tfpdef(self, ident_tok, annotation_opt):
        _all_stmts[(31656,31659)] = True
        """(3.0-) tfpdef: NAME [':' test]"""
        if annotation_opt:
            _all_stmts[(31754,31756)] = True
            colon_loc, annotation = annotation_opt
            return self._arg(ident_tok, colon_loc, annotation)
        return self._arg(ident_tok)

    vfpdef = fpdef_1
    """(3.0-) vfpdef: NAME"""

    @action(List(Rule("fpdef", loc=(31993,31997)), ",", trailing=True, loc=(31988,31992)), loc=(31981,31987))
    def fplist(self, elts):
        _all_stmts[(32033,32036)] = True
        """fplist: fpdef (',' fpdef)* [',']"""
        return ast.Tuple(elts=elts, ctx=None, loc=None)

    stmt = Alt(Rule("simple_stmt", loc=(32176,32180)), Rule("compound_stmt", loc=(32197,32201)), loc=(32172,32175))
    """stmt: simple_stmt | compound_stmt"""

    simple_stmt = SeqN(0, List(Rule("small_stmt", loc=(32296,32300)), ";", trailing=True, loc=(32291,32295)), Tok("newline", loc=(32337,32340)), loc=(32283,32287))
    """simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE"""

    small_stmt = Alt(Rule("expr_stmt", loc=(32441,32445)), Rule("print_stmt", loc=(32460,32464)),  Rule("del_stmt", loc=(32481,32485)),
                     Rule("pass_stmt", loc=(32520,32524)), Rule("flow_stmt", loc=(32539,32543)), Rule("import_stmt", loc=(32558,32562)),
                     Rule("global_stmt", loc=(32600,32604)), Rule("nonlocal_stmt", loc=(32621,32625)), Rule("exec_stmt", loc=(32644,32648)),
                     Rule("assert_stmt", loc=(32684,32688)), loc=(32437,32440))
    """
    (2.6, 2.7)
    small_stmt: (expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | exec_stmt | assert_stmt)
    (3.0-)
    small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | nonlocal_stmt | assert_stmt)
    """

    expr_stmt_1__26 = Rule("testlist", loc=(33056,33060))
    expr_stmt_1__32 = Rule("testlist_star_expr", loc=(33095,33099))

    @action(Seq(Rule("augassign", loc=(33139,33143)), Alt(Rule("yield_expr", loc=(33162,33166)), Rule("testlist", loc=(33182,33186)), loc=(33158,33161)), loc=(33135,33138)), loc=(33128,33134))
    def expr_stmt_2(self, augassign, rhs_expr):
        _all_stmts[(33206,33209)] = True
        return ast.AugAssign(op=augassign, value=rhs_expr)

    @action(Star(Seq(Loc("=", loc=(33331,33334)), Alt(Rule("yield_expr", loc=(33345,33349)), Rule("expr_stmt_1", loc=(33365,33369)), loc=(33341,33344)), loc=(33327,33330)), loc=(33322,33326)), loc=(33315,33321))
    def expr_stmt_3(self, seq):
        _all_stmts[(33393,33396)] = True
        if len(seq) > 0:
            _all_stmts[(33429,33431)] = True
            return ast.Assign(targets=list(map(lambda x: x[1], seq[:-1])), value=seq[-1][1],
                              op_locs=list(map(lambda x: x[0], seq)))
        else:
            _all_stmts[(33617,33621)] = True
            return None

    @action(Seq(Rule("expr_stmt_1", loc=(33664,33668)), Alt(expr_stmt_2, expr_stmt_3, loc=(33685,33688)), loc=(33660,33663)), loc=(33653,33659))
    def expr_stmt(self, lhs, rhs):
        _all_stmts[(33721,33724)] = True
        """
        (2.6, 2.7, 3.0, 3.1)
        expr_stmt: testlist (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist))*)
        (3.2-)
        expr_stmt: testlist_star_expr (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist_star_expr))*)
        """
        if isinstance(rhs, ast.AugAssign):
            _all_stmts[(34092,34094)] = True
            if isinstance(lhs, ast.Tuple) or isinstance(lhs, ast.List):
                _all_stmts[(34139,34141)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "illegal expression for augmented assignment", {},
                    rhs.op.loc, [lhs.loc])
                self.diagnostic_engine.process(error)
            else:
                _all_stmts[(34435,34439)] = True
                rhs.target = self._assignable(lhs)
                rhs.loc = rhs.target.loc.join(rhs.value.loc)
                return rhs
        elif rhs is not None:
            _all_stmts[(34588,34592)] = True
            rhs.targets = list(map(self._assignable, [lhs] + rhs.targets))
            rhs.loc = lhs.loc.join(rhs.value.loc)
            return rhs
        else:
            _all_stmts[(34766,34770)] = True
            return ast.Expr(value=lhs, loc=lhs.loc)

    testlist_star_expr = action(
        List(Alt(Rule("test", loc=(34875,34879)), Rule("star_expr", loc=(34889,34893)), loc=(34871,34874)), ",", trailing=True, loc=(34866,34870)), loc=(34850,34856)) \
        (_wrap_tuple)
    """(3.2-) testlist_star_expr: (test|star_expr) (',' (test|star_expr))* [',']"""

    augassign = Alt(Oper(ast.Add, "+=", loc=(35059,35063)), Oper(ast.Sub, "-=", loc=(35080,35084)), Oper(ast.MatMult, "@=", loc=(35101,35105)),
                    Oper(ast.Mult, "*=", loc=(35146,35150)), Oper(ast.Div, "/=", loc=(35168,35172)), Oper(ast.Mod, "%=", loc=(35189,35193)),
                    Oper(ast.BitAnd, "&=", loc=(35230,35234)), Oper(ast.BitOr, "|=", loc=(35254,35258)), Oper(ast.BitXor, "^=", loc=(35277,35281)),
                    Oper(ast.LShift, "<<=", loc=(35321,35325)), Oper(ast.RShift, ">>=", loc=(35346,35350)),
                    Oper(ast.Pow, "**=", loc=(35391,35395)), Oper(ast.FloorDiv, "//=", loc=(35413,35417)), loc=(35055,35058))
    """augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
                   '<<=' | '>>=' | '**=' | '//=')"""

    @action(List(Rule("test", loc=(35586,35590)), ",", trailing=True, loc=(35581,35585)), loc=(35574,35580))
    def print_stmt_1(self, values):
        _all_stmts[(35625,35628)] = True
        nl, loc = True, values[-1].loc
        if values.trailing_comma:
            _all_stmts[(35704,35706)] = True
            nl, loc = False, values.trailing_comma.loc
        return ast.Print(dest=None, values=values, nl=nl,
                         dest_loc=None, loc=loc)

    @action(Seq(Loc(">>", loc=(35909,35912)), Rule("test", loc=(35920,35924)), Tok(",", loc=(35934,35937)), List(Rule("test", loc=(35949,35953)), ",", trailing=True, loc=(35944,35948)), loc=(35905,35908)), loc=(35898,35904))
    def print_stmt_2(self, dest_loc, dest, comma_tok, values):
        _all_stmts[(35989,35992)] = True
        nl, loc = True, values[-1].loc
        if values.trailing_comma:
            _all_stmts[(36095,36097)] = True
            nl, loc = False, values.trailing_comma.loc
        return ast.Print(dest=dest, values=values, nl=nl,
                         dest_loc=dest_loc, loc=loc)

    @action(Eps(loc=(36300,36303)), loc=(36293,36299))
    def print_stmt_3(self, eps):
        _all_stmts[(36311,36314)] = True
        return ast.Print(dest=None, values=[], nl=True,
                         dest_loc=None, loc=None)

    @action(Seq(Loc("print", loc=(36463,36466)), Alt(print_stmt_1, print_stmt_2, print_stmt_3, loc=(36477,36480)), loc=(36459,36462)), loc=(36452,36458))
    def print_stmt(self, print_loc, stmt):
        _all_stmts[(36529,36532)] = True
        """
        (2.6-2.7)
        print_stmt: 'print' ( [ test (',' test)* [','] ] |
                              '>>' test [ (',' test)+ [','] ] )
        """
        stmt.keyword_loc = print_loc
        if stmt.loc is None:
            _all_stmts[(36778,36780)] = True
            stmt.loc = print_loc
        else:
            _all_stmts[(36840,36844)] = True
            stmt.loc = print_loc.join(stmt.loc)
        return stmt

    @action(Seq(Loc("del", loc=(36931,36934)), List(Rule("expr", loc=(36948,36952)), ",", trailing=True, loc=(36943,36947)), loc=(36927,36930)), loc=(36920,36926))
    def del_stmt(self, stmt_loc, exprs):
        # Python uses exprlist here, but does *not* obey the usual
        # tuple-wrapping semantics, so we embed the rule directly.
        _all_stmts[(36988,36991)] = True
        """del_stmt: 'del' exprlist"""
        return ast.Delete(targets=[self._assignable(expr, is_delete=True) for expr in exprs],
                          loc=stmt_loc.join(exprs[-1].loc), keyword_loc=stmt_loc)

    @action(Loc("pass", loc=(37387,37390)), loc=(37380,37386))
    def pass_stmt(self, stmt_loc):
        _all_stmts[(37404,37407)] = True
        """pass_stmt: 'pass'"""
        return ast.Pass(loc=stmt_loc, keyword_loc=stmt_loc)

    flow_stmt = Alt(Rule("break_stmt", loc=(37548,37552)), Rule("continue_stmt", loc=(37568,37572)), Rule("return_stmt", loc=(37591,37595)),
                    Rule("raise_stmt", loc=(37632,37636)), Rule("yield_stmt", loc=(37652,37656)), loc=(37544,37547))
    """flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt"""

    @action(Loc("break", loc=(37773,37776)), loc=(37766,37772))
    def break_stmt(self, stmt_loc):
        _all_stmts[(37791,37794)] = True
        """break_stmt: 'break'"""
        return ast.Break(loc=stmt_loc, keyword_loc=stmt_loc)

    @action(Loc("continue", loc=(37931,37934)), loc=(37924,37930))
    def continue_stmt(self, stmt_loc):
        _all_stmts[(37952,37955)] = True
        """continue_stmt: 'continue'"""
        return ast.Continue(loc=stmt_loc, keyword_loc=stmt_loc)

    @action(Seq(Loc("return", loc=(38108,38111)), Opt(Rule("testlist", loc=(38127,38131)), loc=(38123,38126)), loc=(38104,38107)), loc=(38097,38103))
    def return_stmt(self, stmt_loc, values):
        _all_stmts[(38151,38154)] = True
        """return_stmt: 'return' [testlist]"""
        loc = stmt_loc
        if values:
            _all_stmts[(38270,38272)] = True
            loc = loc.join(values.loc)
        return ast.Return(value=values,
                          loc=loc, keyword_loc=stmt_loc)

    @action(Rule("yield_expr", loc=(38430,38434)), loc=(38423,38429))
    def yield_stmt(self, expr):
        _all_stmts[(38454,38457)] = True
        """yield_stmt: yield_expr"""
        return ast.Expr(value=expr, loc=expr.loc)

    @action(Seq(Loc("raise", loc=(38586,38589)), Opt(Seq(Rule("test", loc=(38608,38612)),
                                      Opt(Seq(Tok(",", loc=(38668,38671)), Rule("test", loc=(38678,38682)),
                                              Opt(SeqN(1, Tok(",", loc=(38750,38753)), Rule("test", loc=(38760,38764)), loc=(38742,38746)), loc=(38738,38741)), loc=(38664,38667)), loc=(38660,38663)), loc=(38604,38607)), loc=(38600,38603)), loc=(38582,38585)), loc=(38575,38581))
    def raise_stmt__26(self, raise_loc, type_opt):
        _all_stmts[(38785,38788)] = True
        """(2.6, 2.7) raise_stmt: 'raise' [test [',' test [',' test]]]"""
        type_ = inst = tback = None
        loc = raise_loc
        if type_opt:
            _all_stmts[(38974,38976)] = True
            type_, inst_opt = type_opt
            loc = loc.join(type_.loc)
            if inst_opt:
                _all_stmts[(39076,39078)] = True
                _, inst, tback = inst_opt
                loc = loc.join(inst.loc)
                if tback:
                    _all_stmts[(39188,39190)] = True
                    loc = loc.join(tback.loc)
        return ast.Raise(exc=type_, inst=inst, tback=tback, cause=None,
                         keyword_loc=raise_loc, from_loc=None, loc=loc)

    @action(Seq(Loc("raise", loc=(39405,39408)), Opt(Seq(Rule("test", loc=(39427,39431)), Opt(Seq(Loc("from", loc=(39449,39452)), Rule("test", loc=(39462,39466)), loc=(39445,39448)), loc=(39441,39444)), loc=(39423,39426)), loc=(39419,39422)), loc=(39401,39404)), loc=(39394,39400))
    def raise_stmt__30(self, raise_loc, exc_opt):
        _all_stmts[(39485,39488)] = True
        """(3.0-) raise_stmt: 'raise' [test ['from' test]]"""
        exc = from_loc = cause = None
        loc = raise_loc
        if exc_opt:
            _all_stmts[(39663,39665)] = True
            exc, cause_opt = exc_opt
            loc = loc.join(exc.loc)
            if cause_opt:
                _all_stmts[(39760,39762)] = True
                from_loc, cause = cause_opt
                loc = loc.join(cause.loc)
        return ast.Raise(exc=exc, inst=None, tback=None, cause=cause,
                         keyword_loc=raise_loc, from_loc=from_loc, loc=loc)

    import_stmt = Alt(Rule("import_name", loc=(40029,40033)), Rule("import_from", loc=(40050,40054)), loc=(40025,40028))
    """import_stmt: import_name | import_from"""

    @action(Seq(Loc("import", loc=(40137,40140)), Rule("dotted_as_names", loc=(40152,40156)), loc=(40133,40136)), loc=(40126,40132))
    def import_name(self, import_loc, names):
        _all_stmts[(40182,40185)] = True
        """import_name: 'import' dotted_as_names"""
        return ast.Import(names=names,
                          keyword_loc=import_loc, loc=import_loc.join(names[-1].loc))

    @action(Loc(".", loc=(40414,40417)), loc=(40407,40413))
    def import_from_1(self, loc):
        _all_stmts[(40428,40431)] = True
        return 1, loc

    @action(Loc("...", loc=(40493,40496)), loc=(40486,40492))
    def import_from_2(self, loc):
        _all_stmts[(40509,40512)] = True
        return 3, loc

    @action(Seq(Star(Alt(import_from_1, import_from_2, loc=(40583,40586)), loc=(40578,40582)), Rule("dotted_name", loc=(40619,40623)), loc=(40574,40577)), loc=(40567,40573))
    def import_from_3(self, dots, dotted_name):
        _all_stmts[(40645,40648)] = True
        dots_loc, dots_count = None, 0
        if any(dots):
            _all_stmts[(40736,40738)] = True
            dots_loc = dots[0][1].join(dots[-1][1])
            dots_count = sum([count for count, loc in dots])
        return (dots_loc, dots_count), dotted_name

    @action(Plus(Alt(import_from_1, import_from_2, loc=(40932,40935)), loc=(40927,40931)), loc=(40920,40926))
    def import_from_4(self, dots):
        _all_stmts[(40972,40975)] = True
        dots_loc = dots[0][1].join(dots[-1][1])
        dots_count = sum([count for count, loc in dots])
        return (dots_loc, dots_count), None

    @action(Loc("*", loc=(41165,41168)), loc=(41158,41164))
    def import_from_5(self, star_loc):
        _all_stmts[(41179,41182)] = True
        return (None, 0), \
               [ast.alias(name="*", asname=None,
                          name_loc=star_loc, as_loc=None, asname_loc=None, loc=star_loc)], \
               None

    @action(Rule("import_as_names", loc=(41417,41421)), loc=(41410,41416))
    def import_from_6(self, names):
        _all_stmts[(41446,41449)] = True
        return (None, 0), names, None

    @action(Seq(Loc("from", loc=(41533,41536)), Alt(import_from_3, import_from_4, loc=(41546,41549)),
                Loc("import", loc=(41597,41600)), Alt(import_from_5,
                                   Seq(Loc("(", loc=(41670,41673)), Rule("import_as_names", loc=(41680,41684)), Loc(")", loc=(41705,41708)), loc=(41666,41669)),
                                   import_from_6, loc=(41612,41615)), loc=(41529,41532)), loc=(41522,41528))
    def import_from(self, from_loc, module_name, import_loc, names):
        _all_stmts[(41772,41775)] = True
        """
        (2.6, 2.7)
        import_from: ('from' ('.'* dotted_name | '.'+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        (3.0-)
        # note below: the ('.' | '...') is necessary because '...' is tokenized as ELLIPSIS
        import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        """
        (dots_loc, dots_count), dotted_name_opt = module_name
        module_loc = module = None
        if dotted_name_opt:
            _all_stmts[(42386,42388)] = True
            module_loc, module = dotted_name_opt
        lparen_loc, names, rparen_loc = names
        loc = from_loc.join(names[-1].loc)
        if rparen_loc:
            _all_stmts[(42552,42554)] = True
            loc = loc.join(rparen_loc)

        if module == "__future__":
            _all_stmts[(42615,42617)] = True
            self.add_flags([x.name for x in names])

        return ast.ImportFrom(names=names, module=module, level=dots_count,
                              keyword_loc=from_loc, dots_loc=dots_loc, module_loc=module_loc,
                              import_loc=import_loc, lparen_loc=lparen_loc, rparen_loc=rparen_loc,
                              loc=loc)

    @action(Seq(Tok("ident", loc=(43020,43023)), Opt(Seq(Loc("as", loc=(43042,43045)), Tok("ident", loc=(43053,43056)), loc=(43038,43041)), loc=(43034,43037)), loc=(43016,43019)), loc=(43009,43015))
    def import_as_name(self, name_tok, as_name_opt):
        _all_stmts[(43074,43077)] = True
        """import_as_name: NAME ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        loc = name_tok.loc
        if as_name_opt:
            _all_stmts[(43254,43256)] = True
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=name_tok.value, asname=asname_name,
                         loc=loc, name_loc=name_tok.loc, as_loc=as_loc, asname_loc=asname_loc)

    @action(Seq(Rule("dotted_name", loc=(43603,43607)), Opt(Seq(Loc("as", loc=(43632,43635)), Tok("ident", loc=(43643,43646)), loc=(43628,43631)), loc=(43624,43627)), loc=(43599,43602)), loc=(43592,43598))
    def dotted_as_name(self, dotted_name, as_name_opt):
        _all_stmts[(43664,43667)] = True
        """dotted_as_name: dotted_name ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        dotted_name_loc, dotted_name_name = dotted_name
        loc = dotted_name_loc
        if as_name_opt:
            _all_stmts[(43913,43915)] = True
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=dotted_name_name, asname=asname_name,
                         loc=loc, name_loc=dotted_name_loc, as_loc=as_loc, asname_loc=asname_loc)

    import_as_names = List(Rule("import_as_name", loc=(44278,44282)), ",", trailing=True, loc=(44273,44277))
    """import_as_names: import_as_name (',' import_as_name)* [',']"""

    dotted_as_names = List(Rule("dotted_as_name", loc=(44420,44424)), ",", trailing=False, loc=(44415,44419))
    """dotted_as_names: dotted_as_name (',' dotted_as_name)*"""

    @action(List(Tok("ident", loc=(44547,44550)), ".", trailing=False, loc=(44542,44546)), loc=(44535,44541))
    def dotted_name(self, idents):
        _all_stmts[(44587,44590)] = True
        """dotted_name: NAME ('.' NAME)*"""
        return idents[0].loc.join(idents[-1].loc), \
               ".".join(list(map(lambda x: x.value, idents)))

    @action(Seq(Loc("global", loc=(44794,44797)), List(Tok("ident", loc=(44814,44817)), ",", trailing=False, loc=(44809,44813)), loc=(44790,44793)), loc=(44783,44789))
    def global_stmt(self, global_loc, names):
        _all_stmts[(44855,44858)] = True
        """global_stmt: 'global' NAME (',' NAME)*"""
        return ast.Global(names=list(map(lambda x: x.value, names)),
                          name_locs=list(map(lambda x: x.loc, names)),
                          keyword_loc=global_loc, loc=global_loc.join(names[-1].loc))

    @action(Seq(Loc("exec", loc=(45193,45196)), Rule("expr", loc=(45206,45210)),
                Opt(Seq(Loc("in", loc=(45244,45247)), Rule("test", loc=(45255,45259)),
                        Opt(SeqN(1, Loc(",", loc=(45305,45308)), Rule("test", loc=(45315,45319)), loc=(45297,45301)), loc=(45293,45296)), loc=(45240,45243)), loc=(45236,45239)), loc=(45189,45192)), loc=(45182,45188))
    def exec_stmt(self, exec_loc, body, in_opt):
        _all_stmts[(45338,45341)] = True
        """(2.6, 2.7) exec_stmt: 'exec' expr ['in' test [',' test]]"""
        in_loc, globals, locals = None, None, None
        loc = exec_loc.join(body.loc)
        if in_opt:
            _all_stmts[(45551,45553)] = True
            in_loc, globals, locals = in_opt
            if locals:
                _all_stmts[(45619,45621)] = True
                loc = loc.join(locals.loc)
            else:
                _all_stmts[(45685,45689)] = True
                loc = loc.join(globals.loc)
        return ast.Exec(body=body, locals=locals, globals=globals,
                        loc=loc, keyword_loc=exec_loc, in_loc=in_loc)

    @action(Seq(Loc("nonlocal", loc=(45889,45892)), List(Tok("ident", loc=(45911,45914)), ",", trailing=False, loc=(45906,45910)), loc=(45885,45888)), loc=(45878,45884))
    def nonlocal_stmt(self, nonlocal_loc, names):
        _all_stmts[(45952,45955)] = True
        """(3.0-) nonlocal_stmt: 'nonlocal' NAME (',' NAME)*"""
        return ast.Nonlocal(names=list(map(lambda x: x.value, names)),
                            name_locs=list(map(lambda x: x.loc, names)),
                            keyword_loc=nonlocal_loc, loc=nonlocal_loc.join(names[-1].loc))

    @action(Seq(Loc("assert", loc=(46315,46318)), Rule("test", loc=(46330,46334)), Opt(SeqN(1, Tok(",", loc=(46356,46359)), Rule("test", loc=(46366,46370)), loc=(46348,46352)), loc=(46344,46347)), loc=(46311,46314)), loc=(46304,46310))
    def assert_stmt(self, assert_loc, test, msg):
        _all_stmts[(46387,46390)] = True
        """assert_stmt: 'assert' test [',' test]"""
        loc = assert_loc.join(test.loc)
        if msg:
            _all_stmts[(46533,46535)] = True
            loc = loc.join(msg.loc)
        return ast.Assert(test=test, msg=msg,
                          loc=loc, keyword_loc=assert_loc)

    @action(Alt(Rule("if_stmt", loc=(46699,46703)), Rule("while_stmt", loc=(46716,46720)), Rule("for_stmt", loc=(46736,46740)),
                Rule("try_stmt", loc=(46770,46774)), Rule("with_stmt", loc=(46788,46792)), Rule("funcdef", loc=(46807,46811)),
                Rule("classdef", loc=(46840,46844)), Rule("decorated", loc=(46858,46862)), loc=(46695,46698)), loc=(46688,46694))
    def compound_stmt(self, stmt):
        _all_stmts[(46882,46885)] = True
        """compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt |
                          funcdef | classdef | decorated"""
        return [stmt]

    @action(Seq(Loc("if", loc=(47095,47098)), Rule("test", loc=(47106,47110)), Loc(":", loc=(47120,47123)), Rule("suite", loc=(47130,47134)),
                Star(Seq(Loc("elif", loc=(47170,47173)), Rule("test", loc=(47183,47187)), Loc(":", loc=(47197,47200)), Rule("suite", loc=(47207,47211)), loc=(47166,47169)), loc=(47161,47165)),
                Opt(Seq(Loc("else", loc=(47248,47251)), Loc(":", loc=(47261,47264)), Rule("suite", loc=(47271,47275)), loc=(47244,47247)), loc=(47240,47243)), loc=(47091,47094)), loc=(47084,47090))
    def if_stmt(self, if_loc, test, if_colon_loc, body, elifs, else_opt):
        _all_stmts[(47293,47296)] = True
        """if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]"""
        stmt = ast.If(orelse=[],
                      else_loc=None, else_colon_loc=None)

        if else_opt:
            _all_stmts[(47550,47552)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt

        for elif_ in reversed(elifs):
            _all_stmts[(47643,47646)] = True
            stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = elif_
            stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
            if stmt.orelse:
                _all_stmts[(47827,47829)] = True
                stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
            stmt = ast.If(orelse=[stmt],
                          else_loc=None, else_colon_loc=None)

        stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = \
            if_loc, test, if_colon_loc, body
        stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
        if stmt.orelse:
            _all_stmts[(48192,48194)] = True
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
        return stmt

    @action(Seq(Loc("while", loc=(48303,48306)), Rule("test", loc=(48317,48321)), Loc(":", loc=(48331,48334)), Rule("suite", loc=(48341,48345)),
                Opt(Seq(Loc("else", loc=(48380,48383)), Loc(":", loc=(48393,48396)), Rule("suite", loc=(48403,48407)), loc=(48376,48379)), loc=(48372,48375)), loc=(48299,48302)), loc=(48292,48298))
    def while_stmt(self, while_loc, test, while_colon_loc, body, else_opt):
        _all_stmts[(48425,48428)] = True
        """while_stmt: 'while' test ':' suite ['else' ':' suite]"""
        stmt = ast.While(test=test, body=body, orelse=[],
                         keyword_loc=while_loc, while_colon_loc=while_colon_loc,
                         else_loc=None, else_colon_loc=None,
                         loc=while_loc.join(body[-1].loc))
        if else_opt:
            _all_stmts[(48832,48834)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt

    @action(Seq(Loc("for", loc=(49012,49015)), Rule("exprlist", loc=(49024,49028)), Loc("in", loc=(49042,49045)), Rule("testlist", loc=(49053,49057)),
                Loc(":", loc=(49087,49090)), Rule("suite", loc=(49097,49101)),
                Opt(Seq(Loc("else", loc=(49136,49139)), Loc(":", loc=(49149,49152)), Rule("suite", loc=(49159,49163)), loc=(49132,49135)), loc=(49128,49131)), loc=(49008,49011)), loc=(49001,49007))
    def for_stmt(self, for_loc, target, in_loc, iter, for_colon_loc, body, else_opt):
        _all_stmts[(49181,49184)] = True
        """for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]"""
        stmt = ast.For(target=self._assignable(target), iter=iter, body=body, orelse=[],
                       keyword_loc=for_loc, in_loc=in_loc, for_colon_loc=for_colon_loc,
                       else_loc=None, else_colon_loc=None,
                       loc=for_loc.join(body[-1].loc))
        if else_opt:
            _all_stmts[(49644,49646)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt

    @action(Seq(Plus(Seq(Rule("except_clause", loc=(49833,49837)), Loc(":", loc=(49856,49859)), Rule("suite", loc=(49866,49870)), loc=(49829,49832)), loc=(49824,49828)),
                Opt(Seq(Loc("else", loc=(49907,49910)), Loc(":", loc=(49920,49923)), Rule("suite", loc=(49930,49934)), loc=(49903,49906)), loc=(49899,49902)),
                Opt(Seq(Loc("finally", loc=(49971,49974)), Loc(":", loc=(49987,49990)), Rule("suite", loc=(49997,50001)), loc=(49967,49970)), loc=(49963,49966)), loc=(49820,49823)), loc=(49813,49819))
    def try_stmt_1(self, clauses, else_opt, finally_opt):
        _all_stmts[(50019,50022)] = True
        handlers = []
        for clause in clauses:
            _all_stmts[(50103,50106)] = True
            handler, handler.colon_loc, handler.body = clause
            handler.loc = handler.loc.join(handler.body[-1].loc)
            handlers.append(handler)

        else_loc, else_colon_loc, orelse = None, None, []
        loc = handlers[-1].loc
        if else_opt:
            _all_stmts[(50388,50390)] = True
            else_loc, else_colon_loc, orelse = else_opt
            loc = orelse[-1].loc

        finally_loc, finally_colon_loc, finalbody = None, None, []
        if finally_opt:
            _all_stmts[(50566,50568)] = True
            finally_loc, finally_colon_loc, finalbody = finally_opt
            loc = finalbody[-1].loc
        stmt = ast.Try(body=None, handlers=handlers, orelse=orelse, finalbody=finalbody,
                       else_loc=else_loc, else_colon_loc=else_colon_loc,
                       finally_loc=finally_loc, finally_colon_loc=finally_colon_loc,
                       loc=loc)
        return stmt

    @action(Seq(Loc("finally", loc=(51002,51005)), Loc(":", loc=(51018,51021)), Rule("suite", loc=(51028,51032)), loc=(50998,51001)), loc=(50991,50997))
    def try_stmt_2(self, finally_loc, finally_colon_loc, finalbody):
        _all_stmts[(51048,51051)] = True
        return ast.Try(body=None, handlers=[], orelse=[], finalbody=finalbody,
                       else_loc=None, else_colon_loc=None,
                       finally_loc=finally_loc, finally_colon_loc=finally_colon_loc,
                       loc=finalbody[-1].loc)

    @action(Seq(Loc("try", loc=(51399,51402)), Loc(":", loc=(51411,51414)), Rule("suite", loc=(51421,51425)), Alt(try_stmt_1, try_stmt_2, loc=(51436,51439)), loc=(51395,51398)), loc=(51388,51394))
    def try_stmt(self, try_loc, try_colon_loc, body, stmt):
        _all_stmts[(51470,51473)] = True
        """
        try_stmt: ('try' ':' suite
                   ((except_clause ':' suite)+
                    ['else' ':' suite]
                    ['finally' ':' suite] |
                    'finally' ':' suite))
        """
        stmt.keyword_loc, stmt.try_colon_loc, stmt.body = \
            try_loc, try_colon_loc, body
        stmt.loc = stmt.loc.join(try_loc)
        return stmt

    @action(Seq(Loc("with", loc=(51937,51940)), Rule("test", loc=(51950,51954)), Opt(Rule("with_var", loc=(51968,51972)), loc=(51964,51967)), Loc(":", loc=(51987,51990)), Rule("suite", loc=(51997,52001)), loc=(51933,51936)), loc=(51926,51932))
    def with_stmt__26(self, with_loc, context, with_var, colon_loc, body):
        _all_stmts[(52017,52020)] = True
        """(2.6, 3.0) with_stmt: 'with' test [ with_var ] ':' suite"""
        if with_var:
            _all_stmts[(52167,52169)] = True
            as_loc, optional_vars = with_var
            item = ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            _all_stmts[(52404,52408)] = True
            item = ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)
        return ast.With(items=[item], body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))

    with_var = Seq(Loc("as", loc=(52739,52742)), Rule("expr", loc=(52750,52754)), loc=(52735,52738))
    """(2.6, 3.0) with_var: 'as' expr"""

    @action(Seq(Loc("with", loc=(52822,52825)), List(Rule("with_item", loc=(52840,52844)), ",", trailing=False, loc=(52835,52839)), Loc(":", loc=(52881,52884)),
                Rule("suite", loc=(52907,52911)), loc=(52818,52821)), loc=(52811,52817))
    def with_stmt__27(self, with_loc, items, colon_loc, body):
        _all_stmts[(52927,52930)] = True
        """(2.7, 3.1-) with_stmt: 'with' with_item (',' with_item)*  ':' suite"""
        return ast.With(items=items, body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))

    @action(Seq(Rule("test", loc=(53257,53261)), Opt(Seq(Loc("as", loc=(53279,53282)), Rule("expr", loc=(53290,53294)), loc=(53275,53278)), loc=(53271,53274)), loc=(53253,53256)), loc=(53246,53252))
    def with_item(self, context, as_opt):
        _all_stmts[(53311,53314)] = True
        """(2.7, 3.1-) with_item: test ['as' expr]"""
        if as_opt:
            _all_stmts[(53411,53413)] = True
            as_loc, optional_vars = as_opt
            return ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            _all_stmts[(53644,53648)] = True
            return ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)

    @action(Seq(Alt(Loc("as", loc=(53807,53810)), Loc(",", loc=(53818,53821)), loc=(53803,53806)), Rule("test", loc=(53829,53833)), loc=(53799,53802)), loc=(53792,53798))
    def except_clause_1__26(self, as_loc, name):
        _all_stmts[(53848,53851)] = True
        return as_loc, None, name

    @action(Seq(Loc("as", loc=(53944,53947)), Tok("ident", loc=(53955,53958)), loc=(53940,53943)), loc=(53933,53939))
    def except_clause_1__30(self, as_loc, name):
        _all_stmts[(53974,53977)] = True
        return as_loc, name, None

    @action(Seq(Loc("except", loc=(54070,54073)),
                Opt(Seq(Rule("test", loc=(54109,54113)),
                        Opt(Rule("except_clause_1", loc=(54151,54155)), loc=(54147,54150)), loc=(54105,54108)), loc=(54101,54104)), loc=(54066,54069)), loc=(54059,54065))
    def except_clause(self, except_loc, exc_opt):
        _all_stmts[(54184,54187)] = True
        """
        (2.6, 2.7) except_clause: 'except' [test [('as' | ',') test]]
        (3.0-) except_clause: 'except' [test ['as' NAME]]
        """
        type_ = name = as_loc = name_loc = None
        loc = except_loc
        if exc_opt:
            _all_stmts[(54463,54465)] = True
            type_, name_opt = exc_opt
            loc = loc.join(type_.loc)
            if name_opt:
                _all_stmts[(54563,54565)] = True
                as_loc, name_tok, name_node = name_opt
                if name_tok:
                    _all_stmts[(54647,54649)] = True
                    name = name_tok.value
                    name_loc = name_tok.loc
                else:
                    _all_stmts[(54762,54766)] = True
                    name = name_node
                    name_loc = name_node.loc
                loc = loc.join(name_loc)
        return ast.ExceptHandler(type=type_, name=name,
                                 except_loc=except_loc, as_loc=as_loc, name_loc=name_loc,
                                 loc=loc)

    @action(Plus(Rule("stmt", loc=(55097,55101)), loc=(55092,55096)), loc=(55085,55091))
    def suite_1(self, stmts):
        _all_stmts[(55116,55119)] = True
        return reduce(list.__add__, stmts, [])

    suite = Alt(Rule("simple_stmt", loc=(55206,55210)),
                SeqN(2, Tok("newline", loc=(55251,55254)), Tok("indent", loc=(55267,55270)), suite_1, Tok("dedent", loc=(55291,55294)), loc=(55243,55247)), loc=(55202,55205))
    """suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT"""

    # 2.x-only backwards compatibility start
    testlist_safe = action(List(Rule("old_test", loc=(55444,55448)), ",", trailing=False, loc=(55439,55443)), loc=(55432,55438))(_wrap_tuple)
    """(2.6, 2.7) testlist_safe: old_test [(',' old_test)+ [',']]"""

    old_test = Alt(Rule("or_test", loc=(55586,55590)), Rule("old_lambdef", loc=(55603,55607)), loc=(55582,55585))
    """(2.6, 2.7) old_test: or_test | old_lambdef"""

    @action(Seq(Loc("lambda", loc=(55694,55697)), Opt(Rule("varargslist", loc=(55713,55717)), loc=(55709,55712)), Loc(":", loc=(55735,55738)), Rule("old_test", loc=(55745,55749)), loc=(55690,55693)), loc=(55683,55689))
    def old_lambdef(self, lambda_loc, args_opt, colon_loc, body):
        _all_stmts[(55768,55771)] = True
        """(2.6, 2.7) old_lambdef: 'lambda' [varargslist] ':' old_test"""
        if args_opt is None:
            _all_stmts[(55912,55914)] = True
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))
    # 2.x-only backwards compatibility end

    @action(Seq(Rule("or_test", loc=(56258,56262)), Opt(Seq(Loc("if", loc=(56283,56286)), Rule("or_test", loc=(56294,56298)),
                                         Loc("else", loc=(56352,56355)), Rule("test", loc=(56365,56369)), loc=(56279,56282)), loc=(56275,56278)), loc=(56254,56257)), loc=(56247,56253))
    def test_1(self, lhs, rhs_opt):
        _all_stmts[(56386,56389)] = True
        if rhs_opt is not None:
            _all_stmts[(56426,56428)] = True
            if_loc, test, else_loc, orelse = rhs_opt
            return ast.IfExp(test=test, body=lhs, orelse=orelse,
                             if_loc=if_loc, else_loc=else_loc, loc=lhs.loc.join(orelse.loc))
        return lhs

    test = Alt(test_1, Rule("lambdef", loc=(56704,56708)), loc=(56692,56695))
    """test: or_test ['if' or_test 'else' test] | lambdef"""

    test_nocond = Alt(Rule("or_test", loc=(56805,56809)), Rule("lambdef_nocond", loc=(56822,56826)), loc=(56801,56804))
    """(3.0-) test_nocond: or_test | lambdef_nocond"""

    def lambdef_action(self, lambda_loc, args_opt, colon_loc, body):
        _all_stmts[(56906,56909)] = True
        if args_opt is None:
            _all_stmts[(56979,56981)] = True
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))

    lambdef = action(
        Seq(Loc("lambda", loc=(57300,57303)), Opt(Rule("varargslist", loc=(57319,57323)), loc=(57315,57318)), Loc(":", loc=(57341,57344)), Rule("test", loc=(57351,57355)), loc=(57296,57299)), loc=(57280,57286)) \
        (lambdef_action)
    """lambdef: 'lambda' [varargslist] ':' test"""

    lambdef_nocond = action(
        Seq(Loc("lambda", loc=(57486,57489)), Opt(Rule("varargslist", loc=(57505,57509)), loc=(57501,57504)), Loc(":", loc=(57527,57530)), Rule("test_nocond", loc=(57537,57541)), loc=(57482,57485)), loc=(57466,57472)) \
        (lambdef_action)
    """(3.0-) lambdef_nocond: 'lambda' [varargslist] ':' test_nocond"""

    @action(Seq(Rule("and_test", loc=(57675,57679)), Star(Seq(Loc("or", loc=(57702,57705)), Rule("and_test", loc=(57713,57717)), loc=(57698,57701)), loc=(57693,57697)), loc=(57671,57674)), loc=(57664,57670))
    def or_test(self, lhs, rhs):
        _all_stmts[(57738,57741)] = True
        """or_test: and_test ('or' and_test)*"""
        if len(rhs) > 0:
            _all_stmts[(57824,57826)] = True
            return ast.BoolOp(op=ast.Or(),
                              values=[lhs] + list(map(lambda x: x[1], rhs)),
                              loc=lhs.loc.join(rhs[-1][1].loc),
                              op_locs=list(map(lambda x: x[0], rhs)))
        else:
            _all_stmts[(58103,58107)] = True
            return lhs

    @action(Seq(Rule("not_test", loc=(58149,58153)), Star(Seq(Loc("and", loc=(58176,58179)), Rule("not_test", loc=(58188,58192)), loc=(58172,58175)), loc=(58167,58171)), loc=(58145,58148)), loc=(58138,58144))
    def and_test(self, lhs, rhs):
        _all_stmts[(58213,58216)] = True
        """and_test: not_test ('and' not_test)*"""
        if len(rhs) > 0:
            _all_stmts[(58302,58304)] = True
            return ast.BoolOp(op=ast.And(),
                              values=[lhs] + list(map(lambda x: x[1], rhs)),
                              loc=lhs.loc.join(rhs[-1][1].loc),
                              op_locs=list(map(lambda x: x[0], rhs)))
        else:
            _all_stmts[(58582,58586)] = True
            return lhs

    @action(Seq(Oper(ast.Not, "not", loc=(58628,58632)), Rule("not_test", loc=(58650,58654)), loc=(58624,58627)), loc=(58617,58623))
    def not_test_1(self, op, operand):
        _all_stmts[(58673,58676)] = True
        return ast.UnaryOp(op=op, operand=operand,
                           loc=op.loc.join(operand.loc))

    not_test = Alt(not_test_1, Rule("comparison", loc=(58848,58852)), loc=(58832,58835))
    """not_test: 'not' not_test | comparison"""

    comparison_1__26 = Seq(Rule("expr", loc=(58944,58948)), Star(Seq(Rule("comp_op", loc=(58967,58971)), Rule("expr", loc=(58984,58988)), loc=(58963,58966)), loc=(58958,58962)), loc=(58940,58943))
    comparison_1__30 = Seq(Rule("star_expr", loc=(59027,59031)), Star(Seq(Rule("comp_op", loc=(59055,59059)), Rule("star_expr", loc=(59072,59076)), loc=(59051,59054)), loc=(59046,59050)), loc=(59023,59026))
    comparison_1__32 = comparison_1__26

    @action(Rule("comparison_1", loc=(59146,59150)), loc=(59139,59145))
    def comparison(self, lhs, rhs):
        _all_stmts[(59172,59175)] = True
        """
        (2.6, 2.7) comparison: expr (comp_op expr)*
        (3.0, 3.1) comparison: star_expr (comp_op star_expr)*
        (3.2-) comparison: expr (comp_op expr)*
        """
        if len(rhs) > 0:
            _all_stmts[(59398,59400)] = True
            return ast.Compare(left=lhs, ops=list(map(lambda x: x[0], rhs)),
                               comparators=list(map(lambda x: x[1], rhs)),
                               loc=lhs.loc.join(rhs[-1][1].loc))
        else:
            _all_stmts[(59640,59644)] = True
            return lhs

    @action(Seq(Opt(Loc("*", loc=(59690,59693)), loc=(59686,59689)), Rule("expr", loc=(59701,59705)), loc=(59682,59685)), loc=(59675,59681))
    def star_expr__30(self, star_opt, expr):
        _all_stmts[(59720,59723)] = True
        """(3.0, 3.1) star_expr: ['*'] expr"""
        if star_opt:
            _all_stmts[(59816,59818)] = True
            return ast.Starred(value=expr, ctx=None,
                               star_loc=star_opt, loc=expr.loc.join(star_opt))
        return expr

    @action(Seq(Loc("*", loc=(59998,60001)), Rule("expr", loc=(60008,60012)), loc=(59994,59997)), loc=(59987,59993))
    def star_expr__32(self, star_loc, expr):
        _all_stmts[(60027,60030)] = True
        """(3.0-) star_expr: '*' expr"""
        return ast.Starred(value=expr, ctx=None,
                           star_loc=star_loc, loc=expr.loc.join(star_loc))

    comp_op = Alt(Oper(ast.Lt, "<", loc=(60252,60256)), Oper(ast.Gt, ">", loc=(60271,60275)), Oper(ast.Eq, "==", loc=(60290,60294)),
                  Oper(ast.GtE, ">=", loc=(60328,60332)), Oper(ast.LtE, "<=", loc=(60349,60353)), Oper(ast.NotEq, "<>", loc=(60370,60374)),
                  Oper(ast.NotEq, "!=", loc=(60411,60415)),
                  Oper(ast.In, "in", loc=(60452,60456)), Oper(ast.NotIn, "not", "in", loc=(60472,60476)),
                  Oper(ast.IsNot, "is", "not", loc=(60520,60524)), Oper(ast.Is, "is", loc=(60550,60554)), loc=(60248,60251))
    """
    (2.6, 2.7) comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    (3.0-) comp_op: '<'|'>'|'=='|'>='|'<='|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    """

    expr = BinOper("xor_expr", Oper(ast.BitOr, "|", loc=(60787,60791)), loc=(60767,60774))
    """expr: xor_expr ('|' xor_expr)*"""

    xor_expr = BinOper("and_expr", Oper(ast.BitXor, "^", loc=(60886,60890)), loc=(60866,60873))
    """xor_expr: and_expr ('^' and_expr)*"""

    and_expr = BinOper("shift_expr", Oper(ast.BitAnd, "&", loc=(60992,60996)), loc=(60970,60977))
    """and_expr: shift_expr ('&' shift_expr)*"""

    shift_expr = BinOper("arith_expr", Alt(Oper(ast.LShift, "<<", loc=(61108,61112)), Oper(ast.RShift, ">>", loc=(61132,61136)), loc=(61104,61107)), loc=(61082,61089))
    """shift_expr: arith_expr (('<<'|'>>') arith_expr)*"""

    arith_expr = BinOper("term", Alt(Oper(ast.Add, "+", loc=(61254,61258)), Oper(ast.Sub, "-", loc=(61274,61278)), loc=(61250,61253)), loc=(61234,61241))
    """arith_expr: term (('+'|'-') term)*"""

    term = BinOper("factor", Alt(Oper(ast.Mult, "*", loc=(61374,61378)), Oper(ast.MatMult, "@", loc=(61395,61399)),
                                 Oper(ast.Div, "/", loc=(61452,61456)), Oper(ast.Mod, "%", loc=(61472,61476)),
                                 Oper(ast.FloorDiv, "//", loc=(61525,61529)), loc=(61370,61373)), loc=(61352,61359))
    """term: factor (('*'|'/'|'%'|'//') factor)*"""

    @action(Seq(Alt(Oper(ast.UAdd, "+", loc=(61625,61629)), Oper(ast.USub, "-", loc=(61646,61650)), Oper(ast.Invert, "~", loc=(61667,61671)), loc=(61621,61624)),
                Rule("factor", loc=(61707,61711)), loc=(61617,61620)), loc=(61610,61616))
    def factor_1(self, op, factor):
        _all_stmts[(61728,61731)] = True
        return ast.UnaryOp(op=op, operand=factor,
                           loc=op.loc.join(factor.loc))

    factor = Alt(factor_1, Rule("power", loc=(61894,61898)), loc=(61880,61883))
    """factor: ('+'|'-'|'~') factor | power"""

    @action(Seq(Rule("atom", loc=(61973,61977)), Star(Rule("trailer", loc=(61992,61996)), loc=(61987,61991)), Opt(Seq(Loc("**", loc=(62018,62021)), Rule("factor", loc=(62029,62033)), loc=(62014,62017)), loc=(62010,62013)), loc=(61969,61972)), loc=(61962,61968))
    def power(self, atom, trailers, factor_opt):
        _all_stmts[(62052,62055)] = True
        """power: atom trailer* ['**' factor]"""
        for trailer in trailers:
            _all_stmts[(62154,62157)] = True
            if isinstance(trailer, ast.Attribute) or isinstance(trailer, ast.Subscript):
                _all_stmts[(62191,62193)] = True
                trailer.value = atom
            elif isinstance(trailer, ast.Call):
                _all_stmts[(62317,62321)] = True
                trailer.func = atom
            trailer.loc = atom.loc.join(trailer.loc)
            atom = trailer
        if factor_opt:
            _all_stmts[(62477,62479)] = True
            op_loc, factor = factor_opt
            return ast.BinOp(left=atom, op=ast.Pow(loc=op_loc), right=factor,
                             loc=atom.loc.join(factor.loc))
        return atom

    @action(Rule("testlist1", loc=(62703,62707)), loc=(62696,62702))
    def atom_1(self, expr):
        _all_stmts[(62726,62729)] = True
        return ast.Repr(value=expr, loc=None)

    @action(Tok("ident", loc=(62809,62812)), loc=(62802,62808))
    def atom_2(self, tok):
        _all_stmts[(62827,62830)] = True
        return ast.Name(id=tok.value, loc=tok.loc, ctx=None)

    @action(Alt(Tok("int", loc=(62928,62931)), Tok("float", loc=(62940,62943)), Tok("complex", loc=(62954,62957)), Tok("long", loc=(62970,62973)), loc=(62924,62927)), loc=(62917,62923))
    def atom_3(self, tok):
        _all_stmts[(62988,62991)] = True
        return ast.Num(n=tok.value, loc=tok.loc)

    @action(Seq(Tok("strbegin", loc=(63077,63080)), Tok("strdata", loc=(63094,63097)), Tok("strend", loc=(63110,63113)), loc=(63073,63076)), loc=(63066,63072))
    def atom_4(self, begin_tok, data_tok, end_tok):
        _all_stmts[(63130,63133)] = True
        return ast.Str(s=data_tok.value,
                       begin_loc=begin_tok.loc, end_loc=end_tok.loc,
                       loc=begin_tok.loc.join(end_tok.loc))

    @action(Plus(atom_4, loc=(63361,63365)), loc=(63354,63360))
    def atom_5(self, strings):
        _all_stmts[(63379,63382)] = True
        joint = ""
        if all(isinstance(x.s, bytes) for x in strings):
            _all_stmts[(63463,63466)] = True
            joint = b""
        return ast.Str(s=joint.join([x.s for x in strings]),
                       begin_loc=strings[0].begin_loc, end_loc=strings[-1].end_loc,
                       loc=strings[0].loc.join(strings[-1].loc))

    atom_6__26 = Rule("dictmaker", loc=(63734,63738))
    atom_6__27 = Rule("dictorsetmaker", loc=(63769,63773))

    atom__26 = Alt(BeginEnd("(", Opt(Alt(Rule("yield_expr", loc=(63834,63838)), Rule("testlist_comp", loc=(63854,63858)), loc=(63830,63833)), loc=(63826,63829)), ")",
                            empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(63812,63820)),
                   BeginEnd("[", Opt(Rule("listmaker", loc=(64009,64013)), loc=(64005,64008)), "]",
                            empty=lambda self: ast.List(elts=[], ctx=None, loc=None), loc=(63991,63999)),
                   BeginEnd("{", Opt(Rule("atom_6", loc=(64158,64162)), loc=(64154,64157)), "}",
                            empty=lambda self: ast.Dict(keys=[], values=[], colon_locs=[],
                                                        loc=None), loc=(64140,64148)),
                   BeginEnd("`", atom_1, "`", loc=(64358,64366)),
                   atom_2, atom_3, atom_5, loc=(63808,63811))
    """
    (2.6)
    atom: ('(' [yield_expr|testlist_gexp] ')' |
           '[' [listmaker] ']' |
           '{' [dictmaker] '}' |
           '`' testlist1 '`' |
           NAME | NUMBER | STRING+)
    (2.7)
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [listmaker] ']' |
           '{' [dictorsetmaker] '}' |
           '`' testlist1 '`' |
           NAME | NUMBER | STRING+)
    """

    @action(Loc("...", loc=(64845,64848)), loc=(64838,64844))
    def atom_7(self, loc):
        _all_stmts[(64861,64864)] = True
        return ast.Ellipsis(loc=loc)

    @action(Alt(Tok("None", loc=(64938,64941)), Tok("True", loc=(64951,64954)), Tok("False", loc=(64964,64967)), loc=(64934,64937)), loc=(64927,64933))
    def atom_8(self, tok):
        _all_stmts[(64983,64986)] = True
        if tok.kind == "None":
            _all_stmts[(65014,65016)] = True
            value = None
        elif tok.kind == "True":
            _all_stmts[(65070,65074)] = True
            value = True
        elif tok.kind == "False":
            _all_stmts[(65128,65132)] = True
            value = False
        return ast.NameConstant(value=value, loc=tok.loc)

    atom__30 = Alt(BeginEnd("(", Opt(Alt(Rule("yield_expr", loc=(65280,65284)), Rule("testlist_comp", loc=(65300,65304)), loc=(65276,65279)), loc=(65272,65275)), ")",
                            empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(65258,65266)),
                   BeginEnd("[", Opt(Rule("testlist_comp__list", loc=(65455,65459)), loc=(65451,65454)), "]",
                            empty=lambda self: ast.List(elts=[], ctx=None, loc=None), loc=(65437,65445)),
                   BeginEnd("{", Opt(Rule("dictorsetmaker", loc=(65614,65618)), loc=(65610,65613)), "}",
                            empty=lambda self: ast.Dict(keys=[], values=[], colon_locs=[],
                                                        loc=None), loc=(65596,65604)),
                   atom_2, atom_3, atom_5, atom_7, atom_8, loc=(65254,65257))
    """
    (3.0-)
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [testlist_comp] ']' |
           '{' [dictorsetmaker] '}' |
           NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
    """

    def list_gen_action(self, lhs, rhs):
        _all_stmts[(66089,66092)] = True
        if rhs is None: # (x)
            _all_stmts[(66134,66136)] = True
            return lhs
        elif isinstance(rhs, ast.Tuple) or isinstance(rhs, ast.List):
            _all_stmts[(66187,66191)] = True
            rhs.elts = [lhs] + rhs.elts
            return rhs
        elif isinstance(rhs, ast.ListComp) or isinstance(rhs, ast.GeneratorExp):
            _all_stmts[(66320,66324)] = True
            rhs.elt = lhs
            return rhs

    @action(Rule("list_for", loc=(66455,66459)), loc=(66448,66454))
    def listmaker_1(self, compose):
        _all_stmts[(66477,66480)] = True
        return ast.ListComp(generators=compose([]), loc=None)

    @action(List(Rule("test", loc=(66589,66593)), ",", trailing=True, leading=False, loc=(66584,66588)), loc=(66577,66583))
    def listmaker_2(self, elts):
        _all_stmts[(66643,66646)] = True
        return ast.List(elts=elts, ctx=None, loc=None)

    listmaker = action(
        Seq(Rule("test", loc=(66764,66768)),
            Alt(listmaker_1, listmaker_2, loc=(66790,66793)), loc=(66760,66763)), loc=(66744,66750)) \
        (list_gen_action)
    """listmaker: test ( list_for | (',' test)* [','] )"""

    testlist_comp_1__26 = Rule("test", loc=(66936,66940))
    testlist_comp_1__32 = Alt(Rule("test", loc=(66979,66983)), Rule("star_expr", loc=(66993,66997)), loc=(66975,66978))

    @action(Rule("comp_for", loc=(67025,67029)), loc=(67018,67024))
    def testlist_comp_2(self, compose):
        _all_stmts[(67047,67050)] = True
        return ast.GeneratorExp(generators=compose([]), loc=None)

    @action(List(Rule("testlist_comp_1", loc=(67167,67171)), ",", trailing=True, leading=False, loc=(67162,67166)), loc=(67155,67161))
    def testlist_comp_3(self, elts):
        _all_stmts[(67232,67235)] = True
        if elts == [] and not elts.trailing_comma:
            _all_stmts[(67273,67275)] = True
            return None
        else:
            _all_stmts[(67348,67352)] = True
            return ast.Tuple(elts=elts, ctx=None, loc=None)

    testlist_comp = action(
        Seq(Rule("testlist_comp_1", loc=(67455,67459)), Alt(testlist_comp_2, testlist_comp_3, loc=(67480,67483)), loc=(67451,67454)), loc=(67435,67441)) \
        (list_gen_action)
    """
    (2.6) testlist_gexp: test ( gen_for | (',' test)* [','] )
    (2.7, 3.0, 3.1) testlist_comp: test ( comp_for | (',' test)* [','] )
    (3.2-) testlist_comp: (test|star_expr) ( comp_for | (',' (test|star_expr))* [','] )
    """

    @action(Rule("comp_for", loc=(67800,67804)), loc=(67793,67799))
    def testlist_comp__list_1(self, compose):
        _all_stmts[(67822,67825)] = True
        return ast.ListComp(generators=compose([]), loc=None)

    @action(List(Rule("testlist_comp_1", loc=(67944,67948)), ",", trailing=True, leading=False, loc=(67939,67943)), loc=(67932,67938))
    def testlist_comp__list_2(self, elts):
        _all_stmts[(68009,68012)] = True
        return ast.List(elts=elts, ctx=None, loc=None)

    testlist_comp__list = action(
        Seq(Rule("testlist_comp_1", loc=(68150,68154)), Alt(testlist_comp__list_1, testlist_comp__list_2, loc=(68175,68178)), loc=(68146,68149)), loc=(68130,68136)) \
        (list_gen_action)
    """Same grammar as testlist_comp, but different semantic action."""

    @action(Seq(Loc(".", loc=(68344,68347)), Tok("ident", loc=(68354,68357)), loc=(68340,68343)), loc=(68333,68339))
    def trailer_1(self, dot_loc, ident_tok):
        _all_stmts[(68373,68376)] = True
        return ast.Attribute(attr=ident_tok.value, ctx=None,
                             loc=dot_loc.join(ident_tok.loc),
                             attr_loc=ident_tok.loc, dot_loc=dot_loc)

    trailer = Alt(BeginEnd("(", Opt(Rule("arglist", loc=(68644,68648)), loc=(68640,68643)), ")",
                           empty=_empty_arglist, loc=(68626,68634)),
                  BeginEnd("[", Rule("subscriptlist", loc=(68749,68753)), "]", loc=(68735,68743)),
                  trailer_1, loc=(68622,68625))
    """trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME"""

    @action(List(Rule("subscript", loc=(68897,68901)), ",", trailing=True, loc=(68892,68896)), loc=(68885,68891))
    def subscriptlist(self, subscripts):
        _all_stmts[(68941,68944)] = True
        """subscriptlist: subscript (',' subscript)* [',']"""
        if len(subscripts) == 1:
            _all_stmts[(69048,69050)] = True
            return ast.Subscript(slice=subscripts[0], ctx=None, loc=None)
        elif all([isinstance(x, ast.Index) for x in subscripts]):
            _all_stmts[(69155,69159)] = True
            elts  = [x.value for x in subscripts]
            loc   = subscripts[0].loc.join(subscripts[-1].loc)
            index = ast.Index(value=ast.Tuple(elts=elts, ctx=None,
                                              begin_loc=None, end_loc=None, loc=loc),
                              loc=loc)
            return ast.Subscript(slice=index, ctx=None, loc=None)
        else:
            _all_stmts[(69592,69596)] = True
            extslice = ast.ExtSlice(dims=subscripts,
                                    loc=subscripts[0].loc.join(subscripts[-1].loc))
            return ast.Subscript(slice=extslice, ctx=None, loc=None)

    @action(Seq(Loc(".", loc=(69821,69824)), Loc(".", loc=(69831,69834)), Loc(".", loc=(69841,69844)), loc=(69817,69820)), loc=(69810,69816))
    def subscript_1(self, dot_1_loc, dot_2_loc, dot_3_loc):
        _all_stmts[(69856,69859)] = True
        return ast.Ellipsis(loc=dot_1_loc.join(dot_3_loc))

    @action(Seq(Opt(Rule("test", loc=(69992,69996)), loc=(69988,69991)), Loc(":", loc=(70007,70010)), Opt(Rule("test", loc=(70021,70025)), loc=(70017,70020)), Opt(Rule("sliceop", loc=(70040,70044)), loc=(70036,70039)), loc=(69984,69987)), loc=(69977,69983))
    def subscript_2(self, lower_opt, colon_loc, upper_opt, step_opt):
        _all_stmts[(70063,70066)] = True
        loc = colon_loc
        if lower_opt:
            _all_stmts[(70161,70163)] = True
            loc = loc.join(lower_opt.loc)
        if upper_opt:
            _all_stmts[(70225,70227)] = True
            loc = loc.join(upper_opt.loc)
        step_colon_loc = step = None
        if step_opt:
            _all_stmts[(70326,70328)] = True
            step_colon_loc, step = step_opt
            loc = loc.join(step_colon_loc)
            if step:
                _all_stmts[(70438,70440)] = True
                loc = loc.join(step.loc)
        return ast.Slice(lower=lower_opt, upper=upper_opt, step=step,
                         loc=loc, bound_colon_loc=colon_loc, step_colon_loc=step_colon_loc)

    @action(Rule("test", loc=(70663,70667)), loc=(70656,70662))
    def subscript_3(self, expr):
        _all_stmts[(70681,70684)] = True
        return ast.Index(value=expr, loc=expr.loc)

    subscript__26 = Alt(subscript_1, subscript_2, subscript_3, loc=(70782,70785))
    """(2.6, 2.7) subscript: '.' '.' '.' | test | [test] ':' [test] [sliceop]"""

    subscript__30 = Alt(subscript_2, subscript_3, loc=(70927,70930))
    """(3.0-) subscript: test | [test] ':' [test] [sliceop]"""

    sliceop = Seq(Loc(":", loc=(71039,71042)), Opt(Rule("test", loc=(71053,71057)), loc=(71049,71052)), loc=(71035,71038))
    """sliceop: ':' [test]"""

    exprlist_1__26 = List(Rule("expr", loc=(71125,71129)), ",", trailing=True, loc=(71120,71124))
    exprlist_1__30 = List(Rule("star_expr", loc=(71185,71189)), ",", trailing=True, loc=(71180,71184))
    exprlist_1__32 = List(Alt(Rule("expr", loc=(71254,71258)), Rule("star_expr", loc=(71268,71272)), loc=(71250,71253)), ",", trailing=True, loc=(71245,71249))

    @action(Rule("exprlist_1", loc=(71321,71325)), loc=(71314,71320))
    def exprlist(self, exprs):
        _all_stmts[(71345,71348)] = True
        """
        (2.6, 2.7) exprlist: expr (',' expr)* [',']
        (3.0, 3.1) exprlist: star_expr (',' star_expr)* [',']
        (3.2-) exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
        """
        return self._wrap_tuple(exprs)

    @action(List(Rule("test", loc=(71639,71643)), ",", trailing=True, loc=(71634,71638)), loc=(71627,71633))
    def testlist(self, exprs):
        _all_stmts[(71678,71681)] = True
        """testlist: test (',' test)* [',']"""
        return self._wrap_tuple(exprs)

    @action(List(Seq(Rule("test", loc=(71813,71817)), Loc(":", loc=(71827,71830)), Rule("test", loc=(71837,71841)), loc=(71809,71812)), ",", trailing=True, loc=(71804,71808)), loc=(71797,71803))
    def dictmaker(self, elts):
        _all_stmts[(71877,71880)] = True
        """(2.6) dictmaker: test ':' test (',' test ':' test)* [',']"""
        return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                        values=list(map(lambda x: x[2], elts)),
                        colon_locs=list(map(lambda x: x[1], elts)),
                        loc=None)

    dictorsetmaker_1 = Seq(Rule("test", loc=(72232,72236)), Loc(":", loc=(72246,72249)), Rule("test", loc=(72256,72260)), loc=(72228,72231))

    @action(Seq(dictorsetmaker_1,
                Alt(Rule("comp_for", loc=(72325,72329)),
                    List(dictorsetmaker_1, ",", leading=False, trailing=True, loc=(72363,72367)), loc=(72321,72324)), loc=(72283,72286)), loc=(72276,72282))
    def dictorsetmaker_2(self, first, elts):
        _all_stmts[(72428,72431)] = True
        if isinstance(elts, commalist):
            _all_stmts[(72477,72479)] = True
            elts.insert(0, first)
            return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                            values=list(map(lambda x: x[2], elts)),
                            colon_locs=list(map(lambda x: x[1], elts)),
                            loc=None)
        else:
            _all_stmts[(72795,72799)] = True
            return ast.DictComp(key=first[0], value=first[2], generators=elts([]),
                                colon_loc=first[1],
                                begin_loc=None, end_loc=None, loc=None)

    @action(Seq(Rule("test", loc=(73025,73029)),
                Alt(Rule("comp_for", loc=(73059,73063)),
                    List(Rule("test", loc=(73102,73106)), ",", leading=False, trailing=True, loc=(73097,73101)), loc=(73055,73058)), loc=(73021,73024)), loc=(73014,73020))
    def dictorsetmaker_3(self, first, elts):
        _all_stmts[(73158,73161)] = True
        if isinstance(elts, commalist):
            _all_stmts[(73207,73209)] = True
            elts.insert(0, first)
            return ast.Set(elts=elts, loc=None)
        else:
            _all_stmts[(73329,73333)] = True
            return ast.SetComp(elt=first, generators=elts([]),
                               begin_loc=None, end_loc=None, loc=None)

    dictorsetmaker = Alt(dictorsetmaker_2, dictorsetmaker_3, loc=(73491,73494))
    """
    (2.7-)
    dictorsetmaker: ( (test ':' test (comp_for | (',' test ':' test)* [','])) |
                      (test (comp_for | (',' test)* [','])) )
    """

    @action(Seq(Loc("class", loc=(73717,73720)), Tok("ident", loc=(73731,73734)),
                Opt(Seq(Loc("(", loc=(73769,73772)), List(Rule("test", loc=(73784,73788)), ",", trailing=True, loc=(73779,73783)), Loc(")", loc=(73819,73822)), loc=(73765,73768)), loc=(73761,73764)),
                Loc(":", loc=(73847,73850)), Rule("suite", loc=(73857,73861)), loc=(73713,73716)), loc=(73706,73712))
    def classdef__26(self, class_loc, name_tok, bases_opt, colon_loc, body):
        _all_stmts[(73877,73880)] = True
        """(2.6, 2.7) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        bases, lparen_loc, rparen_loc = [], None, None
        if bases_opt:
            _all_stmts[(74092,74094)] = True
            lparen_loc, bases, rparen_loc = bases_opt

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=[],
                            starargs=None, kwargs=None, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=None, dstar_loc=None, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))

    @action(Seq(Loc("class", loc=(74669,74672)), Tok("ident", loc=(74683,74686)),
                Opt(Seq(Loc("(", loc=(74721,74724)), Rule("arglist", loc=(74731,74735)), Loc(")", loc=(74748,74751)), loc=(74717,74720)), loc=(74713,74716)),
                Loc(":", loc=(74776,74779)), Rule("suite", loc=(74786,74790)), loc=(74665,74668)), loc=(74658,74664))
    def classdef__30(self, class_loc, name_tok, arglist_opt, colon_loc, body):
        _all_stmts[(74806,74809)] = True
        """(3.0) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        arglist, lparen_loc, rparen_loc = [], None, None
        bases, keywords, starargs, kwargs = [], [], None, None
        star_loc, dstar_loc = None, None
        if arglist_opt:
            _all_stmts[(75124,75126)] = True
            lparen_loc, arglist, rparen_loc = arglist_opt
            bases, keywords, starargs, kwargs = \
                arglist.args, arglist.keywords, arglist.starargs, arglist.kwargs
            star_loc, dstar_loc = arglist.star_loc, arglist.dstar_loc

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=keywords,
                            starargs=starargs, kwargs=kwargs, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=star_loc, dstar_loc=dstar_loc, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))

    @action(Seq(Loc("*", loc=(75929,75932)), Rule("test", loc=(75939,75943)), Star(SeqN(1, Tok(",", loc=(75966,75969)), Rule("argument", loc=(75976,75980)), loc=(75958,75962)), loc=(75953,75957)),
                Opt(Seq(Tok(",", loc=(76020,76023)), Loc("**", loc=(76030,76033)), Rule("test", loc=(76041,76045)), loc=(76016,76019)), loc=(76012,76015)), loc=(75925,75928)), loc=(75918,75924))
    def arglist_1(self, star_loc, stararg, postargs, kwarg_opt):
        _all_stmts[(76062,76065)] = True
        dstar_loc = kwarg = None
        if kwarg_opt:
            _all_stmts[(76164,76166)] = True
            _, dstar_loc, kwarg = kwarg_opt

        for postarg in postargs:
            _all_stmts[(76231,76234)] = True
            if not isinstance(postarg, ast.keyword):
                _all_stmts[(76268,76270)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "only named arguments may follow *expression", {},
                    postarg.loc, [star_loc.join(stararg.loc)])
                self.diagnostic_engine.process(error)

        return postargs, \
               ast.Call(args=[], keywords=[], starargs=stararg, kwargs=kwarg,
                        star_loc=star_loc, dstar_loc=dstar_loc, loc=None)

    @action(Seq(Loc("**", loc=(76750,76753)), Rule("test", loc=(76761,76765)), loc=(76746,76749)), loc=(76739,76745))
    def arglist_2(self, dstar_loc, kwarg):
        _all_stmts[(76780,76783)] = True
        return [], \
               ast.Call(args=[], keywords=[], starargs=None, kwargs=kwarg,
                        star_loc=None, dstar_loc=dstar_loc, loc=None)

    @action(Seq(Rule("argument", loc=(77002,77006)),
                Alt(SeqN(1, Tok(",", loc=(77048,77051)), Alt(Rule("arglist_1", loc=(77062,77066)),
                                          Rule("arglist_2", loc=(77123,77127)),
                                          Rule("arglist_3", loc=(77184,77188)),
                                          Eps(loc=(77245,77248)), loc=(77058,77061)), loc=(77040,77044)),
                    Eps(loc=(77274,77277)), loc=(77036,77039)), loc=(76998,77001)), loc=(76991,76997))
    def arglist_3(self, arg, cont):
        _all_stmts[(77287,77290)] = True
        if cont is None:
            _all_stmts[(77327,77329)] = True
            return [arg], self._empty_arglist()
        else:
            _all_stmts[(77400,77404)] = True
            args, rest = cont
            return [arg] + args, rest

    @action(Alt(Rule("arglist_1", loc=(77491,77495)),
                Rule("arglist_2", loc=(77526,77530)),
                Rule("arglist_3", loc=(77561,77565)), loc=(77487,77490)), loc=(77480,77486))
    def arglist(self, args, call):
        _all_stmts[(77585,77588)] = True
        """arglist: (argument ',')* (argument [','] |
                                     '*' test (',' argument)* [',' '**' test] |
                                     '**' test)"""
        for arg in args:
            _all_stmts[(77809,77812)] = True
            if isinstance(arg, ast.keyword):
                _all_stmts[(77838,77840)] = True
                call.keywords.append(arg)
            elif len(call.keywords) > 0:
                _all_stmts[(77925,77929)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "non-keyword arg after keyword arg", {},
                    arg.loc, [call.keywords[-1].loc])
                self.diagnostic_engine.process(error)
            else:
                _all_stmts[(78191,78195)] = True
                call.args.append(arg)
        return call

    @action(Seq(Loc("=", loc=(78272,78275)), Rule("test", loc=(78282,78286)), loc=(78268,78271)), loc=(78261,78267))
    def argument_1(self, equals_loc, rhs):
        _all_stmts[(78301,78304)] = True
        def thunk(lhs):
            _all_stmts[(78348,78351)] = True
            if not isinstance(lhs, ast.Name):
                _all_stmts[(78376,78378)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "keyword must be an identifier", {}, lhs.loc)
                self.diagnostic_engine.process(error)
            return ast.keyword(arg=lhs.id, value=rhs,
                               loc=lhs.loc.join(rhs.loc),
                               arg_loc=lhs.loc, equals_loc=equals_loc)
        return thunk

    @action(Opt(Rule("comp_for", loc=(78807,78811)), loc=(78803,78806)), loc=(78796,78802))
    def argument_2(self, compose_opt):
        _all_stmts[(78830,78833)] = True
        def thunk(lhs):
            _all_stmts[(78873,78876)] = True
            if compose_opt:
                _all_stmts[(78901,78903)] = True
                generators = compose_opt([])
                return ast.GeneratorExp(elt=lhs, generators=generators,
                                        begin_loc=None, end_loc=None,
                                        loc=lhs.loc.join(generators[-1].loc))
            return lhs
        return thunk

    @action(Seq(Rule("test", loc=(79243,79247)), Alt(argument_1, argument_2, loc=(79257,79260)), loc=(79239,79242)), loc=(79232,79238))
    def argument(self, lhs, thunk):
        # This rule is reformulated to avoid exponential backtracking.
        _all_stmts[(79291,79294)] = True
        """
        (2.6) argument: test [gen_for] | test '=' test  # Really [keyword '='] test
        (2.7-) argument: test [comp_for] | test '=' test
        """
        return thunk(lhs)

    list_iter = Alt(Rule("list_for", loc=(79606,79610)), Rule("list_if", loc=(79624,79628)), loc=(79602,79605))
    """(2.6, 2.7) list_iter: list_for | list_if"""

    def list_comp_for_action(self, for_loc, target, in_loc, iter, next_opt):
        _all_stmts[(79697,79700)] = True
        def compose(comprehensions):
            _all_stmts[(79778,79781)] = True
            comp = ast.comprehension(
                target=target, iter=iter, ifs=[],
                loc=for_loc.join(iter.loc), for_loc=for_loc, in_loc=in_loc, if_locs=[])
            comprehensions += [comp]
            if next_opt:
                _all_stmts[(80032,80034)] = True
                return next_opt(comprehensions)
            else:
                _all_stmts[(80105,80109)] = True
                return comprehensions
        return compose

    def list_comp_if_action(self, if_loc, cond, next_opt):
        _all_stmts[(80177,80180)] = True
        def compose(comprehensions):
            _all_stmts[(80240,80243)] = True
            comprehensions[-1].ifs.append(cond)
            comprehensions[-1].if_locs.append(if_loc)
            comprehensions[-1].loc = comprehensions[-1].loc.join(cond.loc)
            if next_opt:
                _all_stmts[(80458,80460)] = True
                return next_opt(comprehensions)
            else:
                _all_stmts[(80531,80535)] = True
                return comprehensions
        return compose

    list_for = action(
        Seq(Loc("for", loc=(80634,80637)), Rule("exprlist", loc=(80646,80650)),
            Loc("in", loc=(80676,80679)), Rule("testlist_safe", loc=(80687,80691)), Opt(Rule("list_iter", loc=(80714,80718)), loc=(80710,80713)), loc=(80630,80633)), loc=(80614,80620)) \
        (list_comp_for_action)
    """(2.6, 2.7) list_for: 'for' exprlist 'in' testlist_safe [list_iter]"""

    list_if = action(
        Seq(Loc("if", loc=(80880,80883)), Rule("old_test", loc=(80891,80895)), Opt(Rule("list_iter", loc=(80913,80917)), loc=(80909,80912)), loc=(80876,80879)), loc=(80860,80866)) \
        (list_comp_if_action)
    """(2.6, 2.7) list_if: 'if' old_test [list_iter]"""

    comp_iter = Alt(Rule("comp_for", loc=(81043,81047)), Rule("comp_if", loc=(81061,81065)), loc=(81039,81042))
    """
    (2.6) gen_iter: gen_for | gen_if
    (2.7-) comp_iter: comp_for | comp_if
    """

    comp_for = action(
        Seq(Loc("for", loc=(81208,81211)), Rule("exprlist", loc=(81220,81224)),
            Loc("in", loc=(81250,81253)), Rule("or_test", loc=(81261,81265)), Opt(Rule("comp_iter", loc=(81282,81286)), loc=(81278,81281)), loc=(81204,81207)), loc=(81188,81194)) \
        (list_comp_for_action)
    """
    (2.6) gen_for: 'for' exprlist 'in' or_test [gen_iter]
    (2.7-) comp_for: 'for' exprlist 'in' or_test [comp_iter]
    """

    comp_if__26 = action(
        Seq(Loc("if", loc=(81510,81513)), Rule("old_test", loc=(81521,81525)), Opt(Rule("comp_iter", loc=(81543,81547)), loc=(81539,81542)), loc=(81506,81509)), loc=(81490,81496)) \
        (list_comp_if_action)
    """
    (2.6) gen_if: 'if' old_test [gen_iter]
    (2.7) comp_if: 'if' old_test [comp_iter]
    """

    comp_if__30 = action(
        Seq(Loc("if", loc=(81739,81742)), Rule("test_nocond", loc=(81750,81754)), Opt(Rule("comp_iter", loc=(81775,81779)), loc=(81771,81774)), loc=(81735,81738)), loc=(81719,81725)) \
        (list_comp_if_action)
    """
    (3.0-) comp_if: 'if' test_nocond [comp_iter]
    """

    testlist1 = action(List(Rule("test", loc=(81922,81926)), ",", trailing=False, loc=(81917,81921)), loc=(81910,81916))(_wrap_tuple)
    """testlist1: test (',' test)*"""

    @action(Seq(Loc("yield", loc=(82026,82029)), Opt(Rule("testlist", loc=(82044,82048)), loc=(82040,82043)), loc=(82022,82025)), loc=(82015,82021))
    def yield_expr__26(self, yield_loc, exprs):
        _all_stmts[(82068,82071)] = True
        """(2.6, 2.7, 3.0, 3.1, 3.2) yield_expr: 'yield' [testlist]"""
        if exprs is not None:
            _all_stmts[(82191,82193)] = True
            return ast.Yield(value=exprs,
                             yield_loc=yield_loc, loc=yield_loc.join(exprs.loc))
        else:
            _all_stmts[(82344,82348)] = True
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)

    @action(Seq(Loc("yield", loc=(82473,82476)), Opt(Rule("yield_arg", loc=(82491,82495)), loc=(82487,82490)), loc=(82469,82472)), loc=(82462,82468))
    def yield_expr__33(self, yield_loc, arg):
        _all_stmts[(82516,82519)] = True
        """(3.3-) yield_expr: 'yield' [yield_arg]"""
        if isinstance(arg, ast.YieldFrom):
            _all_stmts[(82619,82621)] = True
            arg.yield_loc = yield_loc
            arg.loc = arg.loc.join(arg.yield_loc)
            return arg
        elif arg is not None:
            _all_stmts[(82773,82777)] = True
            return ast.Yield(value=arg,
                             yield_loc=yield_loc, loc=yield_loc.join(arg.loc))
        else:
            _all_stmts[(82922,82926)] = True
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)

    @action(Seq(Loc("from", loc=(83051,83054)), Rule("test", loc=(83064,83068)), loc=(83047,83050)), loc=(83040,83046))
    def yield_arg_1(self, from_loc, value):
        _all_stmts[(83083,83086)] = True
        return ast.YieldFrom(value=value,
                             from_loc=from_loc, loc=from_loc.join(value.loc))

    yield_arg = Alt(yield_arg_1, Rule("testlist", loc=(83277,83281)), loc=(83260,83263))
    """(3.3-) yield_arg: 'from' test | testlist"""
