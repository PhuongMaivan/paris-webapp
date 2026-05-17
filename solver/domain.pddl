(define (domain isr)
    (:requirements :typing :negative-preconditions :equality)
    (:types loc)
    (:predicates 
        (adj ?l1 ?l2 - loc) 
        (free ?l - loc)
        (tokened ?l - loc)
    )

    (:action jump
        :parameters (?from - loc ?to - loc)
        :precondition (and 
            (tokened ?from) 
            (free ?to)
            (not (adj ?from ?to)) 
            (not (exists (?n - loc) (and (adj ?to ?n) (tokened ?n) (not (= ?n ?from)))))
        )
        :effect (and 
            (not (tokened ?from)) (free ?from)
            (tokened ?to) (not (free ?to))
        )
    )
)