export function testall(suiteName: string, testo: Record<string, () => void>) {
  describe(suiteName, () => {
    for (let [name, f] of Object.entries(testo)) {
      test(name, f);
    }
  });
}

export function qw(s: string): string[] {
  return s.split(/\s+/);
}
