#!/usr/bin/python3.10

class Regexpr:
    "Modélisation d'expression régulières"

    def res(expr):
        "Evaluation d'une expression régulière"
        match expr:
            case Regexpr.Or(expr1,expr2):
                return (Regexpr.res(expr1) or Regexpr.res(expr2))
            case Regexpr.And(expr1,expr2):
                return (res(expr1) and res(expr2))
            case Regexpr.Vide():
                return True
            case Regexpr.Element(expr):
                return expr
            case True:
                return True
            case False:
                return False

    class Or:
        __match_args__ = ("expr1", "expr2") 
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2

    class And:
        __match_args__ = ("expr1", "expr2") 
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2

    class Element:
        __match_args__ = ("expr") 
        def __init__(self,expr):
            self.a = expr

    class Vide:
        def __init__(self):
            pass

expression = Regexpr.And(True,False) or

print(Regexpr.res(expression))

