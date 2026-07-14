import { getEntityColor } from "@/lib/utils";

export function EntityChip({ label, name }: { label: string; name: string }) {
  const color = getEntityColor(label);

  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-(--radius-full) border px-2 py-0.5 text-xs font-medium"
      style={{
        color,
        borderColor: `color-mix(in srgb, ${color} 32%, transparent)`,
        backgroundColor: `color-mix(in srgb, ${color} 12%, transparent)`,
      }}
    >
      {name}
    </span>
  );
}
