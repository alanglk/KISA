struct ProblemaEDOs{ftype,fltype}
    f::ftype
    u0::Vector{fltype}
    tspan::Tuple{fltype,fltype}
    p::Vector{fltype}
end

struct SolucionProblemaEDOs{ftype,fltype}
    t::Vector{fltype}
    u::Vector{Vector{fltype}}
    prob::ProblemaEDOs{ftype,fltype}
end

function Euler(problema::ProblemaEDOs{ftype,fltype}, n::Integer, m::Integer=1) where {ftype<:Function,fltype<:AbstractFloat}
    u0 = problema.u0
    t0, T = problema.tspan
    p = problema.p
    f = problema.f
    #
    h = (T - t0) / (n * m)
    duj = similar(u0)

    tt = [t0]
    uu = [copy(u0)]
    tj = t0
    uj = copy(u0)
    for j in 1:n
        for i in 1:m
            f(duj, tj, uj, p)
            @. uj = uj + h * duj
            tj = tj + h
        end
        push!(tt, tj)
        push!(uu, copy(uj))
    end
    return SolucionProblemaEDOs(tt, uu, problema)
end



function EulerMejorado(problema::ProblemaEDOs{ftype,fltype}, n::Integer, m::Integer=1) where {ftype<:Function,fltype<:AbstractFloat}
    # n: número de soluciones/vectores de estado a calcular
    # m: cada cuántos steps se guarda un vector de estado para el cálculo final
    # En funcion de n y m se calcula h -> 
    #      h: Intervalo de tiempo entre cada una de las soluciones guardadas (si m = 1).
    #         Si no, el intervalo de tiempo entre cada una de las soluciones es h * m

    u0 = problema.u0    # Vector de la solución inicial
    t0, T = problema.tspan # Intervalo de tiempo para calcular la solución aproximada
    p = problema.p     # Vector de parámetros constantes
    f! = problema.f     # Función de modelado del problema | Ecuación diferencial a resolver (en formato vectorial)

    h = (T - t0) / (n * m) # Intervalo de tiempo entre cada una de las soluciones
    tt = [t0]        # Vector de tiempos
    uu = [u0]        # Vector de estados

    tj = copy(t0)     # Inicializar el instante inicial
    uj = copy(u0)     # Inicializar el vector de estado inicial
    uj_ = similar(u0)  # Inicializar como un vector vacío similar a u0
    duj = similar(u0)  # Inicializar como un vector vacío similar a u0
    duj_ = similar(u0)  # Inicializar como un vector vacío similar a u0

    for j in 1:n
        # Para cada solución que queremos guardar
        for i in 1:m
            # Avanzamos m steps en el método de Euler Mejorado
            # *1: Realizar las operaciones componente a componente para evitar crear nuevos vectores

            f!(duj, tj, uj, p)
            @. uj_ = uj + h * duj # *1 
            tj_ = tj + h
            f!(duj_, tj_, uj_, p)
            @. uj = uj + h / 2 * (duj + duj_) # *1
            tj = tj_

        end
        # Guardamos t y u
        push!(tt, copy(tj))
        push!(uu, copy(uj))
    end

    return SolucionProblemaEDOs(tt, uu, problema)
end


function RungeKuta4(problema::ProblemaEDOs{ftype,fltype}, n::Integer, m::Integer=1) where {ftype<:Function,fltype<:AbstractFloat}
    u0 = problema.u0    # Vector de la solución inicial
    t0, T = problema.tspan # Intervalo de tiempo para calcular la solución aproximada
    p = problema.p     # Vector de parámetros constantes
    f! = problema.f     # Función de modelado del problema | Ecuación diferencial a resolver (en formato vectorial)

    h = (T - t0) / (n * m) # Intervalo de tiempo entre cada una de las soluciones
    tt = [t0]        # Vector de tiempos
    uu = [u0]        # Vector de estados

    tj = copy(t0)
    uj = copy(u0)

    uj_ = similar(u0)
    tj_ = similar(u0)
    f1 	= similar(u0)
    f2 	= similar(u0)
    f3 	= similar(u0)
    f4 	= similar(u0)

    for j in 1:n
        # Para cada solución que queremos guardar
        for i in 1:m
            # Avanzamos m steps en el método de Euler Mejorado

            f!(f1, tj, uj, p) # F1

            @. uj_ = uj + h / 2 * f1
            tj_ = tj + h / 2
            f!(f2, tj_, uj_, p) # F2

            @. uj_ = uj + h / 2 * f2
            f!(f3, tj_, uj_, p) # F3

            @. uj_ = uj + h * f3
            tj_ = tj + h
            f!(f4, tj_, uj_, p) # F4

            @. uj = uj + (h / 6) * (f1 + 2 * f2 + 2 * f3 + f4)
            tj = tj_

        end
        # Guardamos t y u
        push!(tt, copy(tj))
        push!(uu, copy(uj))
    end

    return SolucionProblemaEDOs(tt, uu, problema)
end
