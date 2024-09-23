export function testall(suiteName: string, testo: Record<string, () => void>) {
  describe(suiteName, () => {
    for (let [name, f] of Object.entries(testo)) {
      test(name, f);
    }
  });
}
