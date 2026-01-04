#!/bin/bash
set -e
set -e
tsc binary_fusion_tap.ts && node binary_fusion_tap.js
