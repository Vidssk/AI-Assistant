function fmt(value: string | number | null | undefined, suffix = ""): string {
  if (value === null || value === undefined || value === "") return "—";
  return `${value}${suffix}`;
}

export function fmtText(value: string | null | undefined): string {
  if (value === null || value === undefined || value === "") return "—";
  return value;
}

export function fmtMetric(
  value: number | null | undefined,
  suffix = ""
): string {
  return fmt(value, suffix);
}

export function fmtPair(
  used: number | null | undefined,
  total: number | null | undefined,
  unit = ""
): string {
  if (used == null && total == null) return "—";
  return `${fmt(used)}${unit}/${fmt(total)}${unit}`;
}
