def ponderar(valores):
            """
            Valores (list): Lista de tuplas con los valores de h y sus respectivas ponderaciones
            """
            #Normalizar
            hs = [h for h,p in valores]
            hs_min_max = []
            for h in hs:
                try:
                    value = (h-min(hs))/(max(hs)-min(hs))
                except ZeroDivisionError:
                    value = 0
                hs_min_max.append(value)

            ps = [p for h,p in valores]
            ps_pond = [p/sum(ps) for p in ps]

            newValores = [(h,p) for h,p in zip(hs_min_max, ps_pond)]

            return sum([h*p for h,p in newValores])