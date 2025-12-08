# import mylinal as l
# import mymath
# import sympy

# expression_string = "G * m1 * m2 * (r1 - r2) / scal(r1 - r2)**3"

# # def scal(vec: l.Array) -> float:
# #     return vec.l.Array.scal()

# scal = l.Array.scal

# r1_value = l.Array ([1, 2, 3])
# r2_value = l.Array ([4, 5, 6])
# G = 1
# m1 = 1
# m2 = 1

# def lambda_parse_expr(expr: str):
#     try:
#         G, r1, r2, m1, m2 = sympy.symbols('G r1 r2 m1 m2')
#         local_dict = {'G': G, 'r1': r1, 'r2': r2, 'm1': m1, 'm2': m2, 'scal': scal}

#         parsed_expression = sympy.parse_expr(expression_string, local_dict=local_dict)

#         f = sympy.lambdify((G, r1, r2), parsed_expression) # , modules='numpy')

#         return f(mymath.G, r1_value, r2_value)
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# print(lambda_parse_expr(expression_string))

# # substituted_expression = parsed_expression.subs({
# #             G: G_value,
# #             r1: r1_vector,
# #             r2: r2_vector,
# #         })
# # return substituted_expression.evalf()

