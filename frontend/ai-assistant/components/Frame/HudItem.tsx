interface HudItemProps {
  top?: number | string;
  right?: number | string;
  bottom?: number | string;
  left?: number | string;
  backgroundColor?: string;
  color?: string;
  children: React.ReactNode;
}

export function HudItem({
  top,
  right,
  bottom,
  left,
  backgroundColor,
  color,
  children,
}: HudItemProps) {
  return (
    <div
      style={{
        position: "absolute",
        backgroundColor: backgroundColor,
        color: color,
        top,
        right,
        bottom,
        left,
      }}
    >
      {children}
    </div>
  );
}