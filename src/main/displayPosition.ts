import { screen } from "electron";

export function getBottomRightBounds(width: number, height: number) {
  const display = screen.getPrimaryDisplay().workArea;
  return {
    x: Math.round(display.x + display.width - width - 18),
    y: Math.round(display.y + display.height - height - 18)
  };
}
