import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary/10 text-primary border border-primary/20",
        free: "bg-text-tertiary/10 text-text-tertiary border border-text-tertiary/20",
        pro: "bg-accent-blue/10 text-accent-blue border border-accent-blue/20",
        enterprise: "bg-accent-purple/10 text-accent-purple border border-accent-purple/20",
        premium: "bg-gradient-to-r from-primary/20 to-accent-blue/20 text-primary border border-primary/20",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
