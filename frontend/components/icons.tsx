type IconProps = { size?: number; className?: string };

const base = (size: number) => ({
  width: size,
  height: size,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  "aria-hidden": true,
});

export function ChartIcon({ size = 20, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M4 19V9"/><path d="M10 19V5"/><path d="M16 19v-7"/><path d="M22 19H2"/></svg>;
}
export function SparkIcon({ size = 20, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="m12 3-1.4 4.2a2 2 0 0 1-1.3 1.3L5 10l4.3 1.5a2 2 0 0 1 1.3 1.3L12 17l1.4-4.2a2 2 0 0 1 1.3-1.3L19 10l-4.3-1.5a2 2 0 0 1-1.3-1.3L12 3Z"/><path d="m19 16-.6 1.8a1 1 0 0 1-.6.6L16 19l1.8.6a1 1 0 0 1 .6.6L19 22l.6-1.8a1 1 0 0 1 .6-.6L22 19l-1.8-.6a1 1 0 0 1-.6-.6L19 16Z"/></svg>;
}
export function FlaskIcon({ size = 20, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M9 3h6"/><path d="M10 3v5.5L4.7 18a2 2 0 0 0 1.7 3h11.2a2 2 0 0 0 1.7-3L14 8.5V3"/><path d="M7.5 15h9"/></svg>;
}
export function DatabaseIcon({ size = 20, className }: IconProps) {
  return <svg {...base(size)} className={className}><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>;
}
export function ArrowRightIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>;
}
export function InfoIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/></svg>;
}
export function ShieldIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M12 3 5 6v5c0 4.8 2.8 8.2 7 10 4.2-1.8 7-5.2 7-10V6l-7-3Z"/><path d="m9.5 12 1.7 1.7 3.7-4"/></svg>;
}
export function SlidersIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M4 7h10"/><path d="M18 7h2"/><circle cx="16" cy="7" r="2"/><path d="M4 17h2"/><path d="M10 17h10"/><circle cx="8" cy="17" r="2"/></svg>;
}
export function StatusIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><circle cx="12" cy="12" r="8"/><path d="m8.7 12.3 2.1 2.1 4.7-5"/></svg>;
}
export function RefreshIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M20 6v5h-5"/><path d="M4 18v-5h5"/><path d="M18.4 9A7 7 0 0 0 6.2 6.2L4 8"/><path d="M5.6 15A7 7 0 0 0 17.8 17.8L20 16"/></svg>;
}
export function RupeeIcon({ size = 18, className }: IconProps) {
  return <svg {...base(size)} className={className}><path d="M6 5h12"/><path d="M6 9h12"/><path d="M7 5c5 0 7 1.6 7 4s-2.2 4-7 4l7 6"/></svg>;
}
