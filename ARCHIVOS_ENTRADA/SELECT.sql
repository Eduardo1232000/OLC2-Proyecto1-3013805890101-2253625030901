#def p_f_update(t):
 #   ''' f_update: UPDATE name SET set_list_ WHERE condition PTCOMA'''
    #t[0] = SELECT(t[2], t[4], t[6], lexer.lineno, 0)
  #  print("UPDATE")

#def p_set_list(t):
#    ''' set_list: asignacion 
#                | asignacion COMA set_list'''
#    if len(t) == 2:
#        t[0] = [t[1]]
#    else:
#        t[3].insert(0, t[1])
#        t[0] = t[3]

#def p_asignacion(t):
#    ''' asignacion: name IGUAL expresion'''
    #t[0] = (t[1], t[3])

    #SELECT
def p_f_select(t):
    ''' f_select : SELECT select_list FROM name optional_conditions PTCOMA'''
    #t[0] = UPDATE(t[2], t[4], t[6], lexer.lineno, 0)    
    print("INSERT ")

def p_select_list(t):
    ''' select_list : expresion AS name
                    | expresion
                    | MULTIPLICACION '''
    if len(t) == 2:
        t[0] = [t[1]]
    elif len(t) == 3:
        t[0] = [(t[1], t[3])]
    else:
        t[0] = ["*"]

def p_optional_conditions(t):
    ''' optional_conditions : WHERE condition
                           | '''
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = None