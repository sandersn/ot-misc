module Lev :
sig
  type levOp = Sub | Del | Ins
  val window : int -> 'a list -> 'a list list
  val min_list : 'a list -> 'a
  val levenshtein : string -> string -> int list list
  val optimal : int list list -> (levOp * (int * int)) list
end = struct
  open List;;
  type levOp = Sub | Del | Ins;;
  exception Nothing_to_min;;
  exception Terrible_error;;
  let min_list = function
    | [] -> raise Nothing_to_min
    | [x] -> x
    | (x::xs) -> fold_left min x xs;;
  let window n l =
    rev (map rev (fold_left
                   (fun acc x ->
                      (x :: (ExtList.List.take (n-1) (hd acc))) :: acc)
                   [rev (ExtList.List.take n l)]
                   (ExtList.List.drop n l)));;
  let levenshtein_private s1 s2 indel (delete, insert, subst) =
    let table = [ExtList.List.init
                   (String.length s2 + 1)
                   (fun i -> indel * ((String.length s2) - i))] in
      fold_left
        (fun table (c1, i) -> match (table, c1) with
           | ((prev::prevs), c1) ->
               ((fold_left
                 (fun row context -> match (row, context) with
                    | ((last::this), (c2, [jp1;j])) ->
                        (min_list [j + (delete c1);
                                   jp1 + (subst c1 c2);
                                   last + (insert c2)]) :: row
                    | _ -> raise Terrible_error)
                 [i]
                 (combine (ExtString.String.explode s2)
                          (window 2 (rev prev))))
                 :: table)
           | _ -> raise Terrible_error)
        table
        (combine
           (ExtString.String.explode s1)
           (ExtList.List.init (String.length s1) (fun i -> indel * (i+1))))
  let levenshtein s1 s2 =
    levenshtein_private s1 s2 1 ((fun _ -> 1),
                                 (fun _ -> 1),
                                 (fun c1 c2 -> if c1=c2 then 0 else 2))
  let optimal table =
    let rec loop table trail i j = match table with
      | [[]] -> trail
      | [x::xs] as lastrow ->
          (ExtList.List.init (length lastrow - 1)
                             (fun k -> (Ins, (0, k)))) @ trail
      | ([x]::xs) as lastcol ->
          (ExtList.List.init (length lastcol - 1)
                             (fun k -> (Del, (k, 0)))) @ trail
      | (row::xs) ->
          let sub = hd (tl (hd (tl table))) in
          let del = hd (hd (tl table)) in
          let ins = hd (tl (hd table)) in
          let best = min_list [sub; del; ins] in
            if sub = best then
              loop (map tl (tl table)) ((Sub, (i-1, j-1)) :: trail) (i-1) (j-1)
            else if ins = best then
              loop (map tl table) ((Ins, (i, j-1)) :: trail) i (j-1)
            else if del = best then
              loop (tl table) ((Del, (i-1, j)) :: trail) (i-1) j
            else
              raise Terrible_error
      | _ -> raise Terrible_error in
      (*Std.print table;*)
      loop table [] (length table - 1) (length (hd table) - 1)
end
