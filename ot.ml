module Ot = struct
  open Constraints;;
  open Lev;;
  let id_everything = (fun x y -> x=y)
  let id_vc = Constraints.id "voice"
  let id_cont = Constraints.id "contin"
  let id_place = Constraints.id "place";;
  let optimal_print ops =
    List.iter (function
                 | (Lev.Sub, (i,j)) -> print_string "Sub ";
                     print_int i; print_string ",";
                     print_int j; print_newline();
                 | (Lev.Del, (i,j)) -> print_string "Del ";
                     print_int i; print_string ",";
                     print_int j; print_newline();
                 | (Lev.Ins, (i,j)) -> print_string "Ins ";
                     print_int i; print_string ",";
                     print_int j; print_newline()) ops;;
  (*optimal_print (Lev.optimal (Lev.levenshtein "ap" "pbcdpe"));;*)
  print_int (Constraints.eval id_vc "poo" "foo"); print_newline();
  print_int (Constraints.eval id_vc "poo" "boo"); print_newline();
  print_int (Constraints.eval id_vc "poo" "voo"); print_newline();
  print_int (Constraints.eval Constraints.maxIO "poo" "voo"); print_newline();
  print_int (Constraints.eval Constraints.depIO "poo" "voo"); print_newline();
  print_int (Constraints.eval Constraints.depIO "poo" "apoo"); print_newline();
  print_int (Constraints.eval Constraints.maxIO "poo" "apoo"); print_newline();
  print_int (Constraints.eval Constraints.depIO "poo" "oo"); print_newline();
  (* I'm pretty sure this next result is wrong *)
  print_int (Constraints.eval Constraints.maxIO "poo" "oo"); print_newline();
(* This next section is: 1 1 2 2 1 *)
  print_int (Constraints.eval Constraints.maxIO "art" "cat"); print_newline();
  print_int (Constraints.eval Constraints.depIO "art" "cat"); print_newline();
  print_int (Constraints.eval Constraints.maxIO "bad" "dog"); print_newline();
  print_int (Constraints.eval Constraints.depIO "bad" "dog"); print_newline();
  print_int (Constraints.eval Constraints.maxIO "ant" "anti"); print_newline();
  Std.print (Constraints.syllabify (Features.Features.unify "fizbuz"));
;;
end
