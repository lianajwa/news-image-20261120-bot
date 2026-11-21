// news-image-20261120 v2 — "The World in One Day"
// Friday 20 November 2026, 35 stories, front-page format.
// Written from scratch in this session. Node 22+ stdlib only, no network.
// Draws the whole page into a pixel buffer with a small 5x7 bitmap font
// (all-caps newspaper type: clean, no garbled glyphs) and encodes a PNG
// by hand (zlib deflate + CRC32), so two runs are byte-identical.

import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { deflateSync } from 'node:zlib';

const W = 1024;
const H = 1024;
const buf = Buffer.alloc(W * H * 3);

// ---------- palette ----------
const PAPER: RGB = [246, 241, 227];
const INK: RGB = [17, 17, 17];
const RED: RGB = [176, 30, 30];
const BLUE: RGB = [29, 78, 137];
const DARKBLUE: RGB = [16, 32, 64];
const TEAL: RGB = [18, 110, 105];
const GOLD: RGB = [176, 132, 0];
const GREY: RGB = [90, 90, 86];
const WHITE: RGB = [255, 255, 255];
const LIGHT: RGB = [232, 226, 208];
const OCEAN: RGB = [168, 200, 222];
const LAND: RGB = [201, 180, 88];
const GREEN: RGB = [46, 125, 50];
const ORANGE: RGB = [232, 120, 20];
const YELLOW: RGB = [245, 200, 40];
const SKY: RGB = [24, 48, 96];

type RGB = [number, number, number];

// ---------- raster ----------
function px(x: number, y: number, c: RGB): void {
  if (x < 0 || y < 0 || x >= W || y >= H) return;
  const i = (y * W + x) * 3;
  buf[i] = c[0]; buf[i + 1] = c[1]; buf[i + 2] = c[2];
}
function rect(x: number, y: number, w: number, h: number, c: RGB): void {
  for (let j = y; j < y + h; j++) for (let i = x; i < x + w; i++) px(i, j, c);
}
function hline(x: number, y: number, w: number, c: RGB, t = 1): void { rect(x, y, w, t, c); }
function vline(x: number, y: number, h: number, c: RGB, t = 1): void { rect(x, y, t, h, c); }
function line(x0: number, y0: number, x1: number, y1: number, c: RGB, t = 1): void {
  const dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
  const sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
  let err = dx - dy, x = x0, y = y0;
  for (;;) {
    rect(x - Math.floor(t / 2), y - Math.floor(t / 2), t, t, c);
    if (x === x1 && y === y1) break;
    const e2 = 2 * err;
    if (e2 > -dy) { err -= dy; x += sx; }
    if (e2 < dx) { err += dx; y += sy; }
  }
}
function disc(cx: number, cy: number, r: number, c: RGB): void {
  for (let y = -r; y <= r; y++) for (let x = -r; x <= r; x++)
    if (x * x + y * y <= r * r) px(cx + x, cy + y, c);
}
function ring(cx: number, cy: number, r: number, c: RGB, t = 2): void {
  for (let a = 0; a < 360; a += 2) {
    const rad = (a * Math.PI) / 180;
    rect(Math.round(cx + Math.cos(rad) * r), Math.round(cy + Math.sin(rad) * r), t, t, c);
  }
}
function ellipse(cx: number, cy: number, rx: number, ry: number, c: RGB): void {
  for (let y = -ry; y <= ry; y++) for (let x = -rx; x <= rx; x++)
    if ((x * x) / (rx * rx) + (y * y) / (ry * ry) <= 1) px(cx + x, cy + y, c);
}
function poly(points: [number, number][], c: RGB): void {
  // scanline polygon fill
  let minY = H, maxY = 0;
  for (const [, y] of points) { if (y < minY) minY = y; if (y > maxY) maxY = y; }
  for (let y = minY; y <= maxY; y++) {
    const xs: number[] = [];
    for (let i = 0; i < points.length; i++) {
      const [x1, y1] = points[i], [x2, y2] = points[(i + 1) % points.length];
      if ((y1 <= y && y2 > y) || (y2 <= y && y1 > y)) {
        xs.push(Math.round(x1 + ((y - y1) * (x2 - x1)) / (y2 - y1)));
      }
    }
    xs.sort((a, b) => a - b);
    for (let k = 0; k + 1 < xs.length; k += 2)
      for (let x = xs[k]; x <= xs[k + 1]; x++) px(x, y, c);
  }
}
function box(x: number, y: number, w: number, h: number, fill: RGB, border: RGB, bt = 2): void {
  rect(x, y, w, h, fill);
  rect(x, y, w, bt, border); rect(x, y + h - bt, w, bt, border);
  rect(x, y, bt, h, border); rect(x + w - bt, y, bt, h, border);
}

// ---------- 5x7 bitmap font (all caps) ----------
const FONT: Record<string, string[]> = {
  A: ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
  B: ['11110', '10001', '10001', '11110', '10001', '10001', '11110'],
  C: ['01110', '10001', '10000', '10000', '10000', '10001', '01110'],
  D: ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
  E: ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
  F: ['11111', '10000', '10000', '11110', '10000', '10000', '10000'],
  G: ['01110', '10001', '10000', '10111', '10001', '10001', '01111'],
  H: ['10001', '10001', '10001', '11111', '10001', '10001', '10001'],
  I: ['01110', '00100', '00100', '00100', '00100', '00100', '01110'],
  J: ['00111', '00010', '00010', '00010', '00010', '10010', '01100'],
  K: ['10001', '10010', '10100', '11000', '10100', '10010', '10001'],
  L: ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
  M: ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
  N: ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
  O: ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
  P: ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
  Q: ['01110', '10001', '10001', '10001', '10101', '10010', '01101'],
  R: ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
  S: ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
  T: ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
  U: ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
  V: ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
  W: ['10001', '10001', '10001', '10101', '10101', '11011', '10001'],
  X: ['10001', '10001', '01010', '00100', '01010', '10001', '10001'],
  Y: ['10001', '10001', '01010', '00100', '00100', '00100', '00100'],
  Z: ['11111', '00001', '00010', '00100', '01000', '10000', '11111'],
  '0': ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
  '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
  '2': ['01110', '10001', '00001', '00110', '01000', '10000', '11111'],
  '3': ['11111', '00010', '00100', '00010', '00001', '10001', '01110'],
  '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
  '5': ['11111', '10000', '11110', '00001', '00001', '10001', '01110'],
  '6': ['00110', '01000', '10000', '11110', '10001', '10001', '01110'],
  '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
  '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
  '9': ['01110', '10001', '10001', '01111', '00001', '00010', '01100'],
  ' ': ['00000', '00000', '00000', '00000', '00000', '00000', '00000'],
  '.': ['00000', '00000', '00000', '00000', '00000', '01100', '01100'],
  ',': ['00000', '00000', '00000', '00000', '01100', '00100', '01000'],
  ':': ['00000', '01100', '01100', '00000', '01100', '01100', '00000'],
  ';': ['00000', '01100', '01100', '00000', '01100', '00100', '01000'],
  '-': ['00000', '00000', '00000', '01110', '00000', '00000', '00000'],
  '+': ['00000', '00100', '00100', '11111', '00100', '00100', '00000'],
  '%': ['11001', '11010', '00010', '00100', '01000', '01011', '10011'],
  '(': ['00010', '00100', '01000', '01000', '01000', '00100', '00010'],
  ')': ['01000', '00100', '00010', '00010', '00010', '00100', '01000'],
  '/': ['00001', '00010', '00010', '00100', '01000', '01000', '10000'],
  "'": ['00100', '00100', '01000', '00000', '00000', '00000', '00000'],
  '&': ['01100', '10010', '10100', '01000', '10101', '10010', '01101'],
  '!': ['00100', '00100', '00100', '00100', '00100', '00000', '00100'],
  '?': ['01110', '10001', '00001', '00110', '00100', '00000', '00100'],
  '=': ['00000', '00000', '11111', '00000', '11111', '00000', '00000'],
  '$': ['00100', '01111', '10100', '01110', '00101', '11110', '00100'],
  '"': ['01010', '01010', '00000', '00000', '00000', '00000', '00000'],
  '>': ['10000', '01000', '00100', '00010', '00100', '01000', '10000'],
  '<': ['00001', '00010', '00100', '01000', '00100', '00010', '00001'],
};

function textWidth(s: string, scale: number): number {
  return s.length * 6 * scale - scale;
}
function drawText(x: number, y: number, scale: number, s: string, c: RGB, bold = false): void {
  const up = s.toUpperCase();
  let cx = x;
  for (const ch of up) {
    const g = FONT[ch] ?? FONT['?'];
    for (let r = 0; r < 7; r++) for (let col = 0; col < 5; col++) {
      if (g[r][col] === '1') {
        rect(cx + col * scale, y + r * scale, scale, scale, c);
        if (bold) rect(cx + col * scale + 1, y + r * scale, scale, scale, c);
      }
    }
    cx += 6 * scale;
  }
}
function drawTextC(cx: number, y: number, scale: number, s: string, c: RGB, bold = false): void {
  drawText(cx - Math.floor(textWidth(s, scale) / 2), y, scale, s, c, bold);
}
function wrap(text: string, maxChars: number): string[] {
  const words = text.split(' ');
  const lines: string[] = [];
  let cur = '';
  for (const w of words) {
    if (!cur) { cur = w; continue; }
    if (cur.length + 1 + w.length <= maxChars) cur += ' ' + w;
    else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  return lines;
}
function drawPara(x: number, y: number, scale: number, maxChars: number, text: string, c: RGB, lh?: number): number {
  const lines = wrap(text, maxChars);
  const step = lh ?? 7 * scale + 2;
  lines.forEach((ln, i) => drawText(x, y + i * step, scale, ln, c));
  return lines.length;
}

// ---------- illustrations (all hand-drawn here) ----------
// 1. Globe for the masthead.
function drawGlobe(cx: number, cy: number, r: number): void {
  disc(cx, cy, r, BLUE);
  ellipse(cx - 6, cy - 4, 9, 6, GREEN);
  ellipse(cx + 8, cy + 8, 10, 6, GREEN);
  ellipse(cx + 6, cy - 10, 6, 4, GREEN);
  ring(cx, cy, r, INK, 2);
  line(cx - r, cy, cx + r, cy, WHITE, 1);
  line(cx, cy - r, cx, cy + r, WHITE, 1);
  ellipse(cx, cy, Math.floor(r * 0.55), r, WHITE); // meridian hint (outline only effect)
  disc(cx, cy, r - 2, BLUE); // repaint centre, keep ring
  ellipse(cx - 6, cy - 4, 9, 6, GREEN);
  ellipse(cx + 8, cy + 8, 10, 6, GREEN);
  ellipse(cx + 6, cy - 10, 6, 4, GREEN);
  ring(cx, cy, r, INK, 2);
}

// 2. Kyiv lead: night sky, river, three bridge spans, blasts.
function drawKyiv(x: number, y: number, w: number, h: number): void {
  rect(x, y, w, h, SKY);
  for (const [sx, sy] of [[18, 12], [52, 26], [96, 10], [150, 22], [210, 12], [260, 28], [300, 14]] as [number, number][])
    disc(x + sx, y + sy, 2, WHITE);
  // city silhouette
  rect(x + 8, y + 58, 26, 34, DARKBLUE); rect(x + 44, y + 48, 22, 44, DARKBLUE);
  rect(x + 250, y + 54, 24, 38, DARKBLUE); rect(x + 282, y + 62, 20, 30, DARKBLUE);
  // river
  rect(x, y + h - 26, w, 26, [70, 120, 170]);
  // bridge deck + three spans
  line(x + 6, y + h - 34, x + w - 6, y + h - 34, WHITE, 3);
  for (const bx of [70, 160, 250]) {
    line(x + bx, y + h - 34, x + bx + 24, y + h - 34, WHITE, 2);
    line(x + bx, y + h - 34, x + bx + 12, y + h - 52, WHITE, 2);
    line(x + bx + 24, y + h - 34, x + bx + 12, y + h - 52, WHITE, 2);
  }
  // blasts on two spans
  for (const [bx, by] of [[82, y + h - 58], [262, y + h - 56]] as [number, number][]) {
    disc(bx, by, 12, ORANGE); disc(bx, by, 7, YELLOW); disc(bx, by, 3, WHITE);
    for (let a = 0; a < 8; a++) {
      const rad = (a * Math.PI) / 4;
      line(bx, by, Math.round(bx + Math.cos(rad) * 20), Math.round(by + Math.sin(rad) * 20), YELLOW, 2);
    }
  }
  // smoke
  disc(120, y + 34, 10, [150, 150, 150]); disc(132, y + 28, 8, [170, 170, 170]);
  disc(230, y + 40, 9, [150, 150, 150]);
}

// 3. Cyclone Akvan: sea, coast, spiral, rain.
function drawAkvan(x: number, y: number, w: number, h: number): void {
  rect(x, y, w, h, [140, 190, 220]);
  // coast (land on the right)
  poly([[x + 210, y], [x + w, y], [x + w, y + h], [x + 230, y + h], [x + 215, y + 60]], [214, 196, 140]);
  // spiral
  const cx = x + 120, cy = y + 52;
  for (const r of [10, 20, 30, 40, 48]) ring(cx, cy, r, WHITE, 3);
  disc(cx, cy, 8, [90, 90, 90]);
  // spiral arms
  for (let a = 0; a < 300; a += 6) {
    const rad = (a * Math.PI) / 180, r = 10 + a / 6;
    rect(Math.round(cx + Math.cos(rad) * r), Math.round(cy + Math.sin(rad) * r), 3, 3, WHITE);
  }
  // rain
  for (let i = 0; i < 22; i++) {
    const rx = x + 12 + ((i * 37) % (w - 30)), ry = y + 8 + ((i * 23) % (h - 20));
    line(rx, ry, rx - 5, ry + 10, WHITE, 1);
  }
  // rescue boat
  poly([[x + 250, y + h - 22], [x + 300, y + h - 22], [x + 292, y + h - 10], [x + 258, y + h - 10]], ORANGE);
  line(x + 275, y + h - 22, x + 275, y + h - 38, INK, 2);
}

// 4. AI sell-off: falling chart.
function drawSelloff(x: number, y: number, w: number, h: number): void {
  rect(x, y, w, h, WHITE);
  // bars falling
  const bars = [78, 70, 74, 58, 62, 44, 48, 30];
  bars.forEach((bh, i) => {
    const bx = x + 14 + i * 38;
    rect(bx, y + h - 18 - bh, 24, bh, i >= 5 ? RED : [200, 60, 60]);
  });
  // falling line
  line(x + 12, y + 14, x + 90, y + 30, RED, 3);
  line(x + 90, y + 30, x + 170, y + 52, RED, 3);
  line(x + 170, y + 52, x + 250, y + 62, RED, 3);
  line(x + 250, y + 62, x + w - 14, y + 84, RED, 3);
  // arrow head
  poly([[x + w - 14, y + 84], [x + w - 34, y + 76], [x + w - 30, y + 92]], RED);
}

// 5. World map with pins on land.
function drawMap(x: number, y: number, w: number, h: number): void {
  rect(x, y, w, h, OCEAN);
  const P = (pts: [number, number][]): [number, number][] => pts.map(([a, b]) => [x + a, y + b] as [number, number]);
  poly(P([[30, 18], [110, 8], [170, 16], [160, 48], [130, 66], [100, 86], [80, 76], [50, 52], [25, 36]]), LAND); // N America
  poly(P([[140, 92], [175, 86], [190, 106], [175, 142], [155, 146], [140, 122]]), LAND); // S America
  poly(P([[290, 12], [330, 6], [350, 22], [330, 36], [305, 34], [285, 24]]), LAND); // Europe
  poly(P([[290, 48], [335, 44], [350, 66], [340, 106], [315, 132], [295, 102], [285, 72]]), LAND); // Africa
  poly(P([[355, 8], [460, 2], [530, 12], [570, 32], [550, 56], [510, 66], [470, 52], [420, 62], [390, 46], [360, 32]]), LAND); // Asia
  poly(P([[510, 106], [560, 102], [575, 122], [540, 136], [515, 126]]), LAND); // Australia
  poly(P([[170, 2], [200, 0], [205, 10], [180, 12]]), LAND); // Greenland
  // Japan dots
  disc(x + 565, y + 28, 3, LAND); disc(x + 572, y + 38, 3, LAND);
  // pins: [dx, dy, label, lx, ly]
  const pins: [number, number, string, number, number][] = [
    [325, 24, 'KYIV', 315, 2], [470, 52, 'ODISHA', 440, 66], [545, 52, 'TAIWAN', 520, 66],
    [565, 28, 'TOKYO', 540, 14], [535, 30, 'SEOUL', 500, 18], [302, 18, 'BRUSSELS', 240, 2],
    [340, 42, '', 0, 0], [320, 14, '', 0, 0], [372, 44, '', 0, 0],
    [312, 34, '', 0, 0], [325, 100, '', 0, 0],
  ];
  for (const [px2, py2, label, lx, ly] of pins) {
    disc(x + px2, y + py2, 5, RED); disc(x + px2, y + py2, 2, WHITE);
    if (label) drawText(x + lx, y + ly, 1, label, INK, true);
  }
  drawText(x + 8, y + h - 12, 1, 'PINS: KYIV - ODISHA - TAIWAN - TOKYO - SEOUL - BRUSSELS - ANTALYA - POLAND - IRAQ - ITALY - KENYA', INK);
}

// 6. Grid mini-icons, 26x26, each a different little drawing.
function drawIcon(kind: string, x: number, y: number): void {
  rect(x, y, 26, 26, LIGHT);
  rect(x, y, 26, 2, INK); rect(x, y + 24, 26, 2, INK); rect(x, y, 2, 26, INK); rect(x + 24, y, 2, 26, INK);
  switch (kind) {
    case 'deal': // two flags / handshake
      line(x + 5, y + 6, x + 12, y + 6, BLUE, 2); line(x + 14, y + 6, x + 21, y + 6, RED, 2);
      line(x + 5, y + 13, x + 21, y + 13, GOLD, 2); line(x + 5, y + 19, x + 21, y + 19, TEAL, 2);
      break;
    case 'cop': // globe + leaf
      disc(x + 13, y + 13, 8, GREEN); disc(x + 10, y + 11, 3, [120, 200, 120]); disc(x + 16, y + 16, 3, [120, 200, 120]);
      break;
    case 'missile': // falling missile
      line(x + 6, y + 5, x + 20, y + 19, INK, 3);
      poly([[x + 20, y + 19], [x + 14, y + 18], [x + 19, y + 13]], RED);
      disc(x + 5, y + 4, 2, ORANGE);
      break;
    case 'iraq': // building + flag
      rect(x + 6, y + 10, 14, 10, GOLD); rect(x + 9, y + 5, 8, 5, GOLD);
      line(x + 18, y + 5, x + 18, y + 12, INK, 1); rect(x + 18, y + 5, 5, 3, RED);
      break;
    case 'strike': // megaphone
      poly([[x + 5, y + 10], [x + 5, y + 16], [x + 13, y + 18], [x + 13, y + 8]], RED);
      poly([[x + 13, y + 8], [x + 21, y + 5], [x + 21, y + 21], [x + 13, y + 18]], ORANGE);
      break;
    case 'judge': // gavel
      line(x + 6, y + 20, x + 20, y + 6, INK, 2);
      rect(x + 15, y + 4, 8, 4, GOLD); rect(x + 5, y + 20, 12, 2, GOLD);
      break;
    case 'oil': // derrick
      line(x + 8, y + 21, x + 12, y + 5, INK, 2); line(x + 18, y + 21, x + 12, y + 5, INK, 2);
      line(x + 9, y + 16, x + 17, y + 16, INK, 1); line(x + 10, y + 11, x + 15, y + 11, INK, 1);
      disc(x + 13, y + 21, 3, INK);
      break;
    case 'vote': // ballot box
      rect(x + 6, y + 10, 14, 10, BLUE); line(x + 6, y + 10, x + 20, y + 10, WHITE, 2);
      line(x + 10, y + 4, x + 13, y + 9, RED, 2); line(x + 13, y + 9, x + 18, y + 3, RED, 2);
      break;
    case 'cricket': // bat + ball
      line(x + 7, y + 20, x + 17, y + 7, [160, 110, 40], 3);
      disc(x + 19, y + 6, 4, RED);
      break;
    case 'space': // probe + planet
      disc(x + 18, y + 18, 6, [180, 120, 60]); ring(x + 18, y + 18, 9, GOLD, 1);
      disc(x + 8, y + 8, 3, BLUE); line(x + 8, y + 8, x + 13, y + 13, INK, 1);
      break;
  }
}

// ---------- PNG encode (hand-rolled, deterministic) ----------
const CRC_TABLE: number[] = [];
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  CRC_TABLE[n] = c >>> 0;
}
function crc32(b: Buffer): number {
  let c = 0xffffffff;
  for (let i = 0; i < b.length; i++) c = CRC_TABLE[(c ^ b[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(type: string, data: Buffer): Buffer {
  const out = Buffer.alloc(12 + data.length);
  out.writeUInt32BE(data.length, 0);
  out.write(type, 4, 'ascii');
  data.copy(out, 8);
  out.writeUInt32BE(crc32(Buffer.concat([Buffer.from(type, 'ascii'), data])), 8 + data.length);
  return out;
}
function encodePNG(): Buffer {
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4);
  ihdr[8] = 8; ihdr[9] = 2; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  const raw = Buffer.alloc(H * (1 + W * 3));
  for (let y = 0; y < H; y++) {
    raw[y * (1 + W * 3)] = 0;
    buf.copy(raw, y * (1 + W * 3) + 1, y * W * 3, (y + 1) * W * 3);
  }
  const idat = deflateSync(raw, { level: 9 });
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr), chunk('IDAT', idat), chunk('IEND', Buffer.alloc(0)),
  ]);
}

// ---------- page layout ----------
function drawPage(): void {
  rect(0, 0, W, H, PAPER);
  // outer frame
  rect(0, 0, W, 6, INK); rect(0, H - 6, W, 6, INK);
  rect(0, 0, 6, H, INK); rect(W - 6, 0, 6, H, INK);
  rect(10, 10, W - 20, 2, INK);

  // ---- masthead ----
  drawGlobe(52, 44, 24);
  drawText(28, 74, 1, '35 STORIES', INK, true);
  drawText(28, 84, 1, '7 REGIONS', INK, true);
  drawTextC(512, 18, 5, 'THE WORLD IN ONE DAY', INK, true);
  hline(10, 60, W - 20, INK, 3);
  drawTextC(512, 70, 6, 'FRIDAY 20 NOVEMBER 2026', RED, true);
  hline(10, 120, W - 20, INK, 2);

  // ---- numbers strip: 6 boxes ----
  const strip: [string, string, string, RGB][] = [
    ['3', 'BRIDGES HIT', 'IN KYIV', RED],
    ['300,000+', 'EVACUATED', 'BEFORE AKVAN', BLUE],
    ['-6.2%', 'TAIWAN INDEX', 'FRIDAY CLOSE', RED],
    ['100,000', 'YOUTH VISAS', 'A YEAR UK-EU', TEAL],
    ['2.3%', 'JAPAN', 'INFLATION OCT', INK],
    ['118', 'PHILLIPS RUNS', 'VS INDIA', GREEN],
  ];
  strip.forEach(([num, l1, l2, col], i) => {
    const bx = 10 + i * 168;
    box(bx, 126, 164, 62, WHITE, INK, 2);
    drawTextC(bx + 82, 132, 3, num, col, true);
    drawTextC(bx + 82, 157, 2, l1, INK);
    drawTextC(bx + 82, 172, 2, l2, GREY);
  });

  // ---- 3 lead stories ----
  const leads = [
    { x: 10, kick: 'WAR IN UKRAINE', h1: 'KYIV BRIDGES HIT', h2: 'IN NIGHT BARRAGE',
      body: 'ABOUT 110 MISSILES AND 400 DRONES IN 7 WAVES. AT LEAST 9 DEAD. POWER AND WATER CUT IN KYIV.',
      draw: drawKyiv, col: RED },
    { x: 348, kick: "CYCLONE AKVAN - INDIA", h1: 'CYCLONE AKVAN', h2: 'SLAMS INDIA COAST',
      body: 'LANDFALL NEAR GOPALPUR AT 08:00. OVER 300,000 EVACUATED. WINDS TO 110 KM/H. NO DEATHS REPORTED.',
      draw: drawAkvan, col: BLUE },
    { x: 686, kick: 'MARKETS - ASIA', h1: 'AI SELL-OFF SINKS', h2: 'ASIAN MARKETS',
      body: 'TAIWAN -6.2%, ITS WORST WEEK SINCE 1991. SEOUL -5.2%, TOKYO -5.1%. SOFTBANK -16%.',
      draw: drawSelloff, col: RED },
  ];
  for (const L of leads) {
    drawText(L.x, 194, 2, L.kick, L.col, true);
    box(L.x, 212, 328, 104, WHITE, INK, 2);
    L.draw(L.x + 2, 214, 324, 100);
    drawText(L.x, 322, 3, L.h1, INK, true);
    drawText(L.x, 345, 3, L.h2, INK, true);
    drawPara(L.x, 372, 2, 27, L.body, INK, 15);
  }
  vline(342, 192, 248, INK, 1);
  vline(680, 192, 248, INK, 1);
  hline(10, 440, W - 20, INK, 2);

  // ---- map + date check ----
  drawText(10, 448, 2, 'THE WORLD AT A GLANCE', INK, true);
  drawText(640, 448, 2, 'DATE CHECK - NOT FRIDAY', RED, true);
  box(10, 464, 620, 156, WHITE, INK, 2);
  drawMap(14, 468, 612, 148);
  box(640, 464, 374, 156, WHITE, RED, 2);
  drawText(652, 472, 2, 'DATE CHECK: THU, NOT FRI', RED, true);
  const excluded = [
    'ICJ MYANMAR RULING THU 19 NOV',
    'SHENZHEN SUMMIT THU 19 NOV',
    'ANTHROPIC IPO $83 THU 19 NOV',
    'GTA VI LAUNCH THU 19 NOV',
    'VAN GOGH $190.4M THU 19 NOV',
    'VOYAGER 1 THU 19 NOV',
    'SENATE IRAN VOTE THU 19 NOV',
    'NOT YET: MERCURY ORBIT SAT',
  ];
  excluded.forEach((t, i) => {
    const y = 490 + i * 16;
    rect(652, y + 4, 6, 6, RED);
    drawText(664, y, 2, t, INK);
  });

  // ---- grid: 10 more stories ----
  hline(10, 626, W - 20, INK, 2);
  drawText(10, 632, 2, 'MORE FROM FRIDAY - 10 STORIES', INK, true);
  drawText(700, 632, 2, '3 LEADS + 10 HERE = 13', GREY);
  const grid: [string, string][] = [
    ['deal', 'UK-EU RESET DEAL - BRUSSELS SUMMIT'],
    ['cop', 'COP31 LAST DAY ENDS WITHOUT A DEAL'],
    ['missile', 'RUSSIAN MISSILE LANDS IN POLAND'],
    ['iraq', 'IRAQ TROOPS ENTER MILITIA STRONGHOLD'],
    ['strike', 'ITALY GENERAL STRIKE - 100 SQUARES'],
    ['judge', 'KOREA RULING PARTY TO IMPEACH TOP JUDGE'],
    ['oil', 'KENYA DRILLS FIRST OIL WELL'],
    ['vote', 'BUKELE FILES THIRD-TERM BID'],
    ['cricket', 'PHILLIPS 118 AS NZ BEAT INDIA'],
    ['space', 'BEPICOLOMBO REACHES MERCURY'],
  ];
  grid.forEach(([kind, title], i) => {
    const gx = 10 + (i % 2) * 502;
    const gy = 650 + Math.floor(i / 2) * 28;
    drawIcon(kind, gx, gy);
    drawText(gx + 32, gy + 6, 2, title, INK);
  });

  // ---- ALSO: 22 more ----
  hline(10, 794, W - 20, INK, 2);
  drawText(10, 800, 2, 'ALSO ON FRIDAY - 22 MORE STORIES', INK, true);
  drawText(700, 800, 2, '13 + 22 = 35 IN ALL', GREY);
  const also = [
    'LVIV STATION ATTACK KILLS 2', 'RUSSIA SHUTS ESTONIA BORDER',
    'BERLIN STUDENTS STRIKE OVER DRAFT', 'UK GENERAL: CYBER ATTACKS ABROAD',
    'CHINA HOLDS LENDING RATES', 'SOFTBANK FALLS OVER 14% IN A DAY',
    'KOSPI DOWN 7.9% FOR THE WEEK', 'ISRAEL STRIKES SOUTH LEBANON',
    'MIGRANT BOAT SINKS OFF YEMEN, 4 DEAD', 'CANCER PILL SHRINKS TUMOURS 60.7%',
    'ABUJA COURT BLOCKS TINUBU EVIDENCE', 'KAMPALA ENFORCES EBOLA BAN AT RALLY',
    'MALAWI FUEL QUEUES RUN OVERNIGHT', 'AFDB: 22 NATIONS IN DEBT DISTRESS',
    'RUSSELL FASTEST IN WET VEGAS PRACTICE', 'NASDAQ FUTURES DOWN 1.6%',
    'DEMOCRATS QUERY LAW FIRMS FREE WORK', 'PANAMA WANTS COP31 OIL OUTPUT CAP',
    'AUSTRALIA SHARES DOWN 1.8%', 'ATP BACKS PLAYER PAY OVER $350M',
    'LULA MEETS CHIEF RAONI', 'RIO TINTO PLEDGES $370M PANGUNA LEGACY',
  ];
  also.forEach((t, i) => {
    const ax = 10 + (i % 2) * 502;
    const ay = 820 + Math.floor(i / 2) * 15;
    rect(ax, ay + 4, 6, 6, RED);
    drawText(ax + 12, ay, 2, t, INK);
  });

  // ---- footer ----
  hline(10, 988, W - 20, INK, 2);
  disc(44, 999, 8, GOLD); disc(44, 999, 4, YELLOW);
  drawTextC(512, 992, 2, '35 STORIES - 7 REGIONS - 16 HAND-DRAWN PICTURES - FRIDAY 20 NOVEMBER 2026', INK, true);
  drawTextC(512, 1008, 1, 'SOURCES: REUTERS, AP, AFP, BBC, BLOOMBERG, AL JAZEERA, NHK, CNA - ALL FRIDAY 20 NOV 2026.', GREY);
}

// ---------- run ----------
drawPage();
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), encodePNG());
