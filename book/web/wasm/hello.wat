(module
 (type $FUNCSIG$ii (func (param i32) (result i32)))
 (type $FUNCSIG$iii (func (param i32 i32) (result i32)))
 (import "env" "printf" (func $printf (param i32 i32) (result i32)))
 (import "env" "puts" (func $puts (param i32) (result i32)))
 (table 0 anyfunc)
 (memory $0 1)
 (data (i32.const 16) "argv[%i] = %s\n\00")
 (data (i32.const 32) "Hello World\n\00")
 (export "memory" (memory $0))
 (export "main" (func $main))
 (func $main (; 2 ;) (param $0 i32) (param $1 i32) (result i32)
  (local $2 i32)
  (local $3 i32)
  (i32.store offset=4
   (i32.const 0)
   (tee_local $3
    (i32.sub
     (i32.load offset=4
      (i32.const 0)
     )
     (i32.const 16)
    )
   )
  )
  (drop
   (call $puts
    (i32.const 32)
   )
  )
  (block $label$0
   (br_if $label$0
    (i32.lt_s
     (get_local $0)
     (i32.const 1)
    )
   )
   (set_local $2
    (i32.const 0)
   )
   (loop $label$1
    (i32.store offset=4
     (get_local $3)
     (i32.load
      (get_local $1)
     )
    )
    (i32.store
     (get_local $3)
     (get_local $2)
    )
    (drop
     (call $printf
      (i32.const 16)
      (get_local $3)
     )
    )
    (set_local $1
     (i32.add
      (get_local $1)
      (i32.const 4)
     )
    )
    (br_if $label$1
     (i32.ne
      (get_local $0)
      (tee_local $2
       (i32.add
        (get_local $2)
        (i32.const 1)
       )
      )
     )
    )
   )
  )
  (i32.store offset=4
   (i32.const 0)
   (i32.add
    (get_local $3)
    (i32.const 16)
   )
  )
  (i32.const 0)
 )
)
