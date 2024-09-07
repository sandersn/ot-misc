module Constraints :
sig
  type con
  val count : ('a -> bool) -> 'a list -> int
  val countifnot : ('a -> bool) -> 'a list -> int
  val eval : con -> string -> string -> int
  val id : string -> con
  val depInitSigma : con
  val maxIO : con
  val depIO : con
  val onset : con
  val nuc : con
  val syllabify : (string, Features.Features.feature) Hashtbl.t list ->
    (string, Features.Features.feature) Hashtbl.t list list
end = struct
  open Lev;;
  open Features;;
  type con = Faith of (string -> string -> int)
             | Mark of (string -> int)
  let count f l =
    List.fold_left (fun count x -> count + (if (f x) then 1 else 0)) 0 l
  let countifnot f l =
    count (fun x -> not (f x)) l
  let eval c cand input = match c with
    | Faith f -> f input cand
    | Mark f -> f cand
(* Faith *)
  let id feature =
    Faith (fun i o ->
             countifnot
               (fun (_,(i_index, o_index)) ->
                  try (Hashtbl.find (Hashtbl.find Features.phonemes (Char.escaped i.[i_index])) feature) =
                   (Hashtbl.find (Hashtbl.find Features.phonemes (Char.escaped o.[o_index])) feature)
                  with Not_found -> true
               )
               (List.filter
                  (function | (Lev.Sub, _) -> true | _ -> false)
                  (Lev.optimal (Lev.levenshtein i o))))
  let depInitSigma = Faith
    (fun i o ->
       match List.hd (Lev.optimal (Lev.levenshtein i o)) with
         | (Lev.Ins, _) -> 1
         | _ -> 0)
  let depIO = Faith
    (fun i o ->
       count (function | (Lev.Del, _) -> true | _ -> false)
         (Lev.optimal (Lev.levenshtein i o)))
  let maxIO = Faith
    (fun i o ->
       count (function | (Lev.Ins, _) -> true | _ -> false)
         (Lev.optimal (Lev.levenshtein i o)))
(* Mark *)
  let push x lref =
    lref.contents <- x :: lref.contents
  let pop lref =
    lref.contents <- List.tl lref.contents
  let ($) f g = (fun x -> f (g x))
  let syllabify phs =
    if phs = [] then
      []
    else
      let phs = ref phs in
      let prev = ref (Hashtbl.create 1) in
      let ph = ref (List.hd phs.contents) in
      let acc = ref [] in
      let syllables = ref [] in
      let state = ref "" in
      let advanceCons () =
        pop phs;
        ph.contents <- List.hd phs.contents;
        if Features.True = Hashtbl.find ph.contents "cons" then
          (push acc.contents syllables;
           acc.contents <- [];
           state.contents <- "C")
        else
          state.contents <- "V" in
      let advanceVowel () =
        pop phs;
        ph.contents <- List.hd phs.contents;
        if Features.False = Hashtbl.find ph.contents "cons" then
          (prev.contents <- Hashtbl.create 1;
           push acc.contents syllables;
           acc.contents <- [];
           state.contents <- "V")
        else
          (prev.contents <- ph.contents;
           try
             pop phs;
             ph.contents <- List.hd phs.contents;
             if Features.True = Hashtbl.find ph.contents "cons" then
               state.contents <- "CC"
             else
               (push acc.contents syllables;
                acc.contents <- [];
                state.contents <- "CV");
           with Failure f ->
             push prev.contents acc;
             raise (Failure f)) in
        if Features.True = Hashtbl.find ph.contents "cons" then
          state.contents <- "C"
        else
          state.contents <- "V";
        (try
          while true do
            match state.contents with
              | "C" -> (push ph.contents acc;
                        advanceCons())
              | "V" -> (push ph.contents acc;
                        advanceVowel())
              | "CC" -> (push prev.contents acc;
                         push acc.contents syllables;
                         acc.contents <- [ph.contents];
                         advanceCons())
              | "CV" -> (push prev.contents acc;
                         push ph.contents acc;
                         advanceVowel())
              | _ -> raise Not_found (* Catastrophical: bad state *)
          done
        with Failure f ->
          push acc.contents syllables);
        syllables.contents;;
  let onset = Mark (fun o ->
    count ((=) Features.False)
      (List.map
         (fun syll -> Hashtbl.find (List.hd syll) "cons")
         (syllabify (Features.unify o))))
  let nuc = Mark (fun o ->
    count not
      (List.map
         (not $ List.exists (fun ph -> Hashtbl.find ph "cons"=Features.False))
         (syllabify (Features.unify o))))
end
