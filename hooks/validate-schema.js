#!/usr/bin/env node
//
// Post-edit schema validation hook for Claude Code.
//
// Validates JSON-LD after file edits. Exit codes:
//   0  nothing to report (or nothing to validate)
//   1  warnings only; the edit proceeds
//   2  critical errors; the edit is blocked
//
// Hook configuration lives in hooks/hooks.json:
//
//   {
//     "type": "command",
//     "command": "node",
//     "args": [
//       "${CLAUDE_PLUGIN_ROOT}/hooks/validate-schema.js",
//       "${tool_input.file_path}"
//     ]
//   }
//
// The matcher filters by tool name only (Edit, Write). This script checks
// whether the file actually contains schema markup before validating.
//
// This hook runs on Node, which the harness guarantees, so it starts no
// subprocess and requires no interpreter resolution.
"use strict";

const fs = require("fs");
const path = require("path");

// Files bigger than this are skipped to bound memory and hook latency. Real
// source files almost never exceed it; bigger inputs are typically generated
// bundles or accidental binary writes.
const MAX_FILE_BYTES = 10 * 1024 * 1024; // 10 MiB

const VALID_EXTENSIONS = [".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".php", ".ejs"];

const JSONLD_BLOCK = /<script\s+type=["']application\/ld\+json["']\s*>([\s\S]*?)<\/script>/gi;

const PLACEHOLDERS = [
  "[Business Name]",
  "[City]",
  "[State]",
  "[Phone]",
  "[Address]",
  "[Your",
  "[INSERT",
  "REPLACE",
  "[URL]",
  "[Email]",
];

const DEPRECATED_TYPES = {
  HowTo: "deprecated September 2023",
  SpecialAnnouncement: "deprecated July 31, 2025",
  CourseInfo: "retired June 2025",
  EstimatedSalary: "retired June 2025",
  LearningVideo: "retired June 2025",
  ClaimReview: "retired June 2025; fact-check rich results discontinued",
  VehicleListing: "retired June 2025; vehicle listing structured data discontinued",
};

// Restricted types used incorrectly. FAQPage is intentionally NOT flagged:
// Google retired FAQ rich results for all sites (May 7, 2026), but FAQPage
// remains a valid Schema.org type. This project makes no claim of a confirmed
// AI or ranking benefit.
const RESTRICTED_TYPES = {};

const CRITICAL_KEYWORDS = ["placeholder", "deprecated", "retired"];

function validateSchemaObject(obj, blockNum) {
  const errors = [];
  const prefix = `Block ${blockNum}`;

  if (!Object.prototype.hasOwnProperty.call(obj, "@context")) {
    errors.push(`${prefix}: Missing @context`);
  } else if (obj["@context"] !== "https://schema.org" && obj["@context"] !== "http://schema.org") {
    errors.push(`${prefix}: @context should be 'https://schema.org'`);
  }

  if (!Object.prototype.hasOwnProperty.call(obj, "@type")) {
    errors.push(`${prefix}: Missing @type`);
  }

  const text = JSON.stringify(obj).toLowerCase();
  for (const placeholder of PLACEHOLDERS) {
    if (text.includes(placeholder.toLowerCase())) {
      errors.push(`${prefix}: Contains placeholder text: ${placeholder}`);
    }
  }

  const schemaType = obj["@type"] || "";
  if (Object.prototype.hasOwnProperty.call(DEPRECATED_TYPES, schemaType)) {
    errors.push(`${prefix}: @type '${schemaType}' is ${DEPRECATED_TYPES[schemaType]}`);
  }
  if (Object.prototype.hasOwnProperty.call(RESTRICTED_TYPES, schemaType)) {
    errors.push(
      `${prefix}: @type '${schemaType}' is ${RESTRICTED_TYPES[schemaType]}; verify site qualifies`,
    );
  }

  return errors;
}

function validateJsonld(content) {
  const errors = [];
  let blockNum = 0;
  let match;

  JSONLD_BLOCK.lastIndex = 0;
  while ((match = JSONLD_BLOCK.exec(content)) !== null) {
    blockNum += 1;
    const block = match[1].trim();

    let data;
    try {
      data = JSON.parse(block);
    } catch (error) {
      errors.push(`Block ${blockNum}: Invalid JSON; ${error.message}`);
      continue;
    }

    if (Array.isArray(data)) {
      for (const item of data) {
        if (item && typeof item === "object") {
          errors.push(...validateSchemaObject(item, blockNum));
        }
      }
    } else if (data && typeof data === "object") {
      errors.push(...validateSchemaObject(data, blockNum));
    }
  }

  return errors;
}

// File path comes from argv (exec-form template) or from the stdin hook-event
// JSON. Claude Code's documented hook contract delivers the event on stdin; the
// argv template is kept for harnesses that substitute it. Whichever yields an
// existing file wins.
function resolveFilepath() {
  const [, , argvPath] = process.argv;
  if (argvPath && isFile(argvPath)) {
    return argvPath;
  }

  if (process.stdin.isTTY) {
    return null;
  }

  let raw;
  try {
    raw = fs.readFileSync(0, "utf8");
  } catch {
    return null;
  }
  if (!raw.trim()) {
    return null;
  }

  try {
    const event = JSON.parse(raw);
    const filePath = event && event.tool_input && event.tool_input.file_path;
    if (filePath && isFile(filePath)) {
      return filePath;
    }
  } catch {
    return null;
  }

  return null;
}

function isFile(candidate) {
  try {
    return fs.statSync(candidate).isFile();
  } catch {
    return false;
  }
}

function main() {
  const filepath = resolveFilepath();
  if (!filepath) {
    process.exit(0);
  }

  if (!VALID_EXTENSIONS.includes(path.extname(filepath).toLowerCase())) {
    process.exit(0);
  }

  let content;
  try {
    if (fs.statSync(filepath).size > MAX_FILE_BYTES) {
      process.exit(0);
    }
    content = fs.readFileSync(filepath, "utf8");
  } catch {
    process.exit(0);
  }

  const errors = validateJsonld(content);
  if (errors.length === 0) {
    process.exit(0);
  }

  const critical = errors.filter((error) =>
    CRITICAL_KEYWORDS.some((keyword) => error.toLowerCase().includes(keyword)),
  );
  const warnings = errors.filter((error) => !critical.includes(error));

  if (warnings.length > 0) {
    console.log("⚠️  Schema validation warnings:");
    for (const warning of warnings) {
      console.log(`  - ${warning}`);
    }
  }

  if (critical.length > 0) {
    console.log("🛑 Schema validation ERRORS (blocking):");
    for (const error of critical) {
      console.log(`  - ${error}`);
    }
    process.exit(2); // Block the edit
  }

  process.exit(1); // Warnings only; proceed
}

main();
