module Features :
sig
  type place = Labial | Coronal | Palatal | Velar | Uvular | Dorsal
  type feature = True | False | Place of place
  val phonemes : (string, (string, feature) Hashtbl.t) Hashtbl.t
  val unify : string -> (string, feature) Hashtbl.t list
end
  = struct
    type place = Labial | Coronal | Palatal | Velar | Uvular | Dorsal
        (* Warning! Velar is only used for dark ls and uvular is never used *)
    type feature = True | False | Place of place;;
    let phonemes = Hashtbl.create 100;;
    let freeStringMap f s =
      let acc = ref [] in
        String.iter (fun c -> acc.contents <- (f c) :: acc.contents) s;
        List.rev acc.contents;;
    let unify = freeStringMap (fun c -> Hashtbl.find phonemes (Char.escaped c));;
    let h = Hashtbl.create 20;;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ə" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ɛ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ɜ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɟ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" True;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ɑ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ð" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʋ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "ɔ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɖ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "ø" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" True;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "ɒ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "œ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɹ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ɸ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɻ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɽ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ŋ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɾ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɱ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɰ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɳ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɲ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ç" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɴ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ɨ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" True;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "æ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ɪ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɭ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ɬ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ɯ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "h" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɣ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɢ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɦ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʝ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʟ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʙ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Velar);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɫ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add h "constr gl" True;
    Hashtbl.add phonemes "ʔ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "RTR" True;
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʕ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ɮ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʐ" h;
    Hashtbl.clear h;
    Hashtbl.add h "boundary" True;
    Hashtbl.add phonemes "#" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʒ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "θ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʎ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "ʏ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ʈ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "ʉ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "ʊ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "χ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ʰ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "β" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʀ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "ʁ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ʂ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ʃ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" False;
    Hashtbl.add h "low" True;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "a" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "ʌ" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "c" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "b" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "e" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "d" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "g" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "f" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" False;
    Hashtbl.add phonemes "i" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "RTR" True;
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "ħ" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "k" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" False;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "j" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "m" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "l" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "o" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "nasal" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "n" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "q" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "p" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "s" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "r" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" True;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "u" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" False;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "t" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "lateral" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "w" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Labial);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "v" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" True;
    Hashtbl.add h "cons" False;
    Hashtbl.add h "back" False;
    Hashtbl.add h "son" True;
    Hashtbl.add h "high" True;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "ATR" True;
    Hashtbl.add h "low" False;
    Hashtbl.add h "round" True;
    Hashtbl.add phonemes "y" h;
    Hashtbl.clear h;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Dorsal);
    Hashtbl.add h "strid" False;
    Hashtbl.add h "voice" False;
    Hashtbl.add phonemes "x" h;
    Hashtbl.clear h;
    Hashtbl.add h "anterior" True;
    Hashtbl.add h "approx" False;
    Hashtbl.add h "cons" True;
    Hashtbl.add h "son" False;
    Hashtbl.add h "contin" True;
    Hashtbl.add h "place" (Place Coronal);
    Hashtbl.add h "strid" True;
    Hashtbl.add h "voice" True;
    Hashtbl.add phonemes "z" h;
    phonemes;;
  end
