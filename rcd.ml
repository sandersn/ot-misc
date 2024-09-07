open List;;
let bifilter pred l =
  let rec loop t f l = match l with
      [] -> (t,f)
    | x::xs -> if pred x then loop (x::t) f xs else loop t (x::f) xs
  in
    loop [] [] l
let rec transpose ls = match (hd ls) with
    [] -> []
  | _ -> map hd ls :: transpose (map tl ls)
let filterby f proxy l = rev
  (let rec loop proxy l acc = match proxy with
       [] -> acc
     | x::xs -> if f x then
           loop xs (tl l) ((hd l) :: acc)
       else
           loop xs (tl l) acc
   in
     loop proxy l [])

let nonLosFav = for_all (fun i -> i>=0)
let inactive = for_all (fun i -> i==0)
let filterRows
    (promote : (string * int list) list)
    (demote : (string * int list) list) =
  let titles = map fst demote
  and rows = transpose (map snd demote) in
    combine titles (transpose (filterby inactive (transpose (map snd promote)) rows))
let compose f g x = f (g x)
let rec rcd (cols : (string * int list) list) =
  let promote, demote = bifilter (compose nonLosFav snd) cols in
    if promote==[] or demote==[] then
      [map fst cols]
    else
      (map fst promote) :: (rcd (filterRows promote demote))
