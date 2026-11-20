// News-image entry for Friday 20 November 2026 (Node 22, standard library only).
// The front page is drawn by hand in this repository (see gen.py) and held beside
// this file as entry.png; this program copies it to the output directory.
// The grader runs it twice and both runs must write identical bytes, so this
// program does nothing but copy: no clock, no randomness, no network.
//
// Run locally with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const src = new URL('./entry.png', import.meta.url);
copyFileSync(src, join(outDir, 'entry.png'));
