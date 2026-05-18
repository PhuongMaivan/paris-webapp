(define (domain isr)
    (:requirements :typing :negative-preconditions)
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
            
            ;; DÒNG CẦN THÊM: Cấm nhảy đến đỉnh kề trực tiếp với đỉnh xuất phát
            (not (adj ?from ?to)) 
            
            ;; Đảm bảo điểm đến không kề với bất kỳ token nào khác
            (not (exists (?n - loc) (and (adj ?to ?n) (tokened ?n) (not (= ?n ?from)))))
        )
        :effect (and 
            (not (tokened ?from)) (free ?from)
            (tokened ?to) (not (free ?to))
        )
    )
)