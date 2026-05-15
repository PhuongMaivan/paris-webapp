(define (domain isr)
  (:requirements :strips :negative-preconditions)
  (:predicates
    (free ?l)
    (tokened ?l)
    (handfree)
    (holding)
  )
  (:action pick-l1
    :parameters ()
    :precondition (and (tokened l1) (handfree))
    :effect (and (not (tokened l1)) (free l1) (not (handfree)) (holding))
  )
  (:action place-l1
    :parameters ()
    :precondition (and (holding) (free l1) (free l2) (free l6))
    :effect (and (not (holding)) (tokened l1) (handfree) (not (free l1)))
  )
  (:action pick-l2
    :parameters ()
    :precondition (and (tokened l2) (handfree))
    :effect (and (not (tokened l2)) (free l2) (not (handfree)) (holding))
  )
  (:action place-l2
    :parameters ()
    :precondition (and (holding) (free l2) (free l1) (free l3))
    :effect (and (not (holding)) (tokened l2) (handfree) (not (free l2)))
  )
  (:action pick-l3
    :parameters ()
    :precondition (and (tokened l3) (handfree))
    :effect (and (not (tokened l3)) (free l3) (not (handfree)) (holding))
  )
  (:action place-l3
    :parameters ()
    :precondition (and (holding) (free l3) (free l2) (free l4))
    :effect (and (not (holding)) (tokened l3) (handfree) (not (free l3)))
  )
  (:action pick-l4
    :parameters ()
    :precondition (and (tokened l4) (handfree))
    :effect (and (not (tokened l4)) (free l4) (not (handfree)) (holding))
  )
  (:action place-l4
    :parameters ()
    :precondition (and (holding) (free l4) (free l3) (free l5))
    :effect (and (not (holding)) (tokened l4) (handfree) (not (free l4)))
  )
  (:action pick-l5
    :parameters ()
    :precondition (and (tokened l5) (handfree))
    :effect (and (not (tokened l5)) (free l5) (not (handfree)) (holding))
  )
  (:action place-l5
    :parameters ()
    :precondition (and (holding) (free l5) (free l4) (free l6))
    :effect (and (not (holding)) (tokened l5) (handfree) (not (free l5)))
  )
  (:action pick-l6
    :parameters ()
    :precondition (and (tokened l6) (handfree))
    :effect (and (not (tokened l6)) (free l6) (not (handfree)) (holding))
  )
  (:action place-l6
    :parameters ()
    :precondition (and (holding) (free l6) (free l1) (free l5))
    :effect (and (not (holding)) (tokened l6) (handfree) (not (free l6)))
  )
)
