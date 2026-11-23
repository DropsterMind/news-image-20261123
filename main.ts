// news-image-20261123: one image summing up Monday 23 November 2026.
//
// The poster itself (entry.png, 1024x1024, 120 KB) was drawn by draw.py
// in this repository with flat shapes and DejaVu text, so every headline
// is crisp and nothing in it is garbled. This program only has one job:
// copy that exact file to the grader's output directory, unchanged.
//
// Node 22, standard library only: nothing is installed before it runs,
// there is no network access, and the copy is byte-for-byte identical
// on every run, so the two grader runs write the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`missing image next to this program: ${source}`);
}

const bytes = readFileSync(source);
const pngMagic = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const isPng = pngMagic.every((byte, i) => bytes[i] === byte);
if (!isPng) {
  throw new Error('entry.png is not a PNG file');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`image is ${width}x${height}, over the 1024x1024 limit`);
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`image is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Re-read what was written and confirm it is the same whole PNG:
// a partial or altered copy must fail loudly instead of being judged.
const written = readFileSync(target);
if (written.length !== bytes.length || !written.equals(bytes)) {
  throw new Error('copied file differs from entry.png');
}

const copied = statSync(target);
if (copied.size !== bytes.length) {
  throw new Error(`copied ${copied.size} bytes, expected ${bytes.length}`);
}
console.log(`wrote ${target} (${width}x${height}, ${copied.size} bytes)`);
