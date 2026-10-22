# Capture Phase A mathematical verification evidence on Windows PowerShell.
# Run from any folder inside the repository: .\scripts\capture_phase_a.ps1
# Prerequisites: commit Lake's generated lockfile, install Lean/Lake, and have Git.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location -LiteralPath $root

foreach ($command in @("git", "lean", "lake")) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Missing '$command'. Install it and retry."
    }
}

$revision = (& git rev-parse HEAD | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $revision -notmatch '^[a-f0-9]{40}$') {
    throw "Cannot identify an exact repository revision."
}

# Generated Lake dependencies are ignored. The tracked Lean source and manifest
# must nevertheless be clean to bind a passing proof to an immutable Git revision.
$dirty = @(& git status --porcelain -- "formal/lean")
if ($LASTEXITCODE -ne 0) { throw "Could not inspect Git status." }
if ($dirty.Count -ne 0) {
    Write-Host ($dirty -join [Environment]::NewLine)
    throw "The formal/lean tree contains uncommitted changes. Review and commit lake-manifest.json (or other relevant changes) before collecting evidence."
}

$leanDir = Join-Path $root "formal/lean"
$lockFile = Join-Path $leanDir "lake-manifest.json"
if (-not (Test-Path -LiteralPath $lockFile)) {
    throw "Missing formal/lean/lake-manifest.json"
}

$leanSources = @((Join-Path $leanDir "CRPI.lean")) + @(
    Get-ChildItem -LiteralPath (Join-Path $leanDir "CRPI") -Filter "*.lean" -File |
        ForEach-Object { $_.FullName }
)
$forbidden = @($leanSources | Select-String -Pattern '(?<![a-zA-Z0-9_])(sorry|admit|axiom|unsafe|native_decide)(?![a-zA-Z0-9_])')
if ($forbidden.Count -gt 0) {
    $forbidden | ForEach-Object { Write-Host ("{0}:{1}: {2}" -f $_.Path, $_.LineNumber, $_.Line.Trim()) }
    throw "Forbidden proof shortcut found in theorem-bearing Lean source."
}

$evidence = Join-Path $root ("verification/evidence/" + $revision)
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$buildLog = Join-Path $evidence "lake-build.log"
$auditLog = Join-Path $evidence "axiom-audit.log"

# Elan may select a different compiler from the repository root.
# Read the pinned project toolchain without triggering the root compiler.
$declaredToolchain = (Get-Content -LiteralPath (Join-Path $leanDir "lean-toolchain") -Raw).Trim()
$toolchainMatch = [regex]::Match($declaredToolchain, '^leanprover/lean4:(v[0-9]+\.[0-9]+\.[0-9]+)$')
if (-not $toolchainMatch.Success) {
    throw "Expected an explicit Lean version pin in formal/lean/lean-toolchain."
}
$expectedLeanVersion = $toolchainMatch.Groups[1].Value.Substring(1)
$lockHash = (Get-FileHash -LiteralPath $lockFile -Algorithm SHA256).Hash.ToLowerInvariant()
$lock = Get-Content -LiteralPath $lockFile -Raw | ConvertFrom-Json
$mathlibLock = @($lock.packages | Where-Object { $_.name -eq "mathlib" })
if ($mathlibLock.Count -ne 1) {
    throw "Expected one Mathlib dependency in lake-manifest.json."
}
$mathlibDir = Join-Path $leanDir ".lake/packages/mathlib"
if (-not (Test-Path -LiteralPath $mathlibDir)) {
    throw "Mathlib is not installed. Run lake update and lake exe cache get."
}
$mathlibRevision = (& git -C $mathlibDir rev-parse HEAD | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw "Cannot read the installed Mathlib revision." }
if ($mathlibRevision -ne $mathlibLock[0].rev) {
    throw "Installed Mathlib revision $mathlibRevision does not match the Lake manifest pin $($mathlibLock[0].rev)."
}

$required = @(
    "CRPI.bounded_complement",
    "CRPI.bounded_mul",
    "CRPI.weightedSum_bounded",
    "CRPI.consequenceSeverity_bounded",
    "CRPI.effectiveConsequence_bounded",
    "CRPI.hazard_bounded",
    "CRPI.mitigation_bounded",
    "CRPI.instantaneousResidual_bounded",
    "CRPI.envelope_bounded",
    "CRPI.envelope_mono_residual",
    "CRPI.envelope_mono_stock"
)
$buildExit = -1
$auditExit = -1
Push-Location -LiteralPath $leanDir
try {
    $leanVersion = (& lake env lean --version | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Cannot query the effective project Lean version." }
    $lakeVersion = (& lake --version | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Cannot query the effective project Lake version." }
    if (-not $leanVersion.Contains("Lean (version $expectedLeanVersion,")) {
        throw "Effective project Lean is '$leanVersion', but the pinned toolchain requires $expectedLeanVersion."
    }
    & lake build *> $buildLog
    $buildExit = $LASTEXITCODE
    if ($buildExit -ne 0) {
        throw "lake build failed (exit $buildExit). See $buildLog"
    }
    & lake env lean CRPI/Audit.lean *> $auditLog
    $auditExit = $LASTEXITCODE
    if ($auditExit -ne 0) {
        throw "Axiom audit failed (exit $auditExit). See $auditLog"
    }
}
finally {
    Pop-Location
}

$auditOutput = Get-Content -LiteralPath $auditLog -Raw
$actual = [regex]::Matches(
    $auditOutput,
    "'(?<name>CRPI\.[^']+)' depends on axioms: \[(?<axioms>[^\]]*)\]"
)
$actualNames = @($actual | ForEach-Object { $_.Groups["name"].Value })
$missing = @($required | Where-Object { $_ -notin $actualNames })
if ($missing.Count -gt 0) {
    throw "Axiom audit omitted required theorems: $($missing -join ', ')"
}
$allowedAxioms = @("propext", "Classical.choice", "Quot.sound")
$detectedAxioms = @(
    $actual | ForEach-Object { $_.Groups["axioms"].Value.Split(",") } |
        ForEach-Object { $_.Trim() } | Where-Object { $_ } | Sort-Object -Unique
)
$unexpected = @($detectedAxioms | Where-Object { $_ -notin $allowedAxioms })
if ($unexpected.Count -gt 0) {
    throw "Unexpected axioms: $($unexpected -join ', ')"
}

$summary = [ordered]@{
    evidence_type = "local_machine_checked_lean_phase_a"
    protocol = "CRPI-FVP-001"
    source_commit = $revision
    captured_utc = [DateTime]::UtcNow.ToString("o")
    platform = [Environment]::OSVersion.VersionString
    lean_version = $leanVersion
    lake_version = $lakeVersion
    declared_toolchain = $declaredToolchain
    mathlib_commit = $mathlibRevision
    lake_manifest_sha256 = $lockHash
    commands = @("lake build", "lake env lean CRPI/Audit.lean")
    exit_codes = @{ build = $buildExit; axiom_audit = $auditExit }
    theorem_count = $required.Count
    theorem_names = $required
    permitted_axioms = $allowedAxioms
    observed_axioms = $detectedAxioms
    manual_statement_review = "PASS for Phase A conditional claims; see formal/lean/PHASE_A_STATEMENT_REVIEW.md"
    status = "BUILD_AXIOM_AND_PHASE_A_STATEMENT_REVIEW_PASS"
}
$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $evidence "summary.json") -Encoding utf8

Write-Host "Phase A local machine check passed for source revision: $revision"
Write-Host "Effective project toolchain: $leanVersion"
Write-Host "Recorded $($required.Count) theorems and permitted foundational axioms."
Write-Host "Evidence folder: $evidence"
Write-Host "Next: inspect the artifacts, review statement correspondence, and commit the evidence under verification/evidence."
