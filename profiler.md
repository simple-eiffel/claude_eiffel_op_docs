# Eiffel Profiler Documentation

## Overview

The EiffelStudio profiler instruments compiled Eiffel code to collect performance data during execution. This enables identification of performance bottlenecks by measuring:
- Number of calls to each feature
- Time spent in each feature (self-time)
- Time spent in called features (descendant-time)
- Percentage of total execution time

## Enabling Profiling

### In ECF File

Add to your target's settings:
```xml
<setting name="profile" value="true"/>
```

### In EiffelStudio GUI

1. Project Settings > Target > Advanced Options
2. Check "Profile" checkbox
3. Recompile (freeze or finalize)

## Compilation Modes

| Mode | Use Case | Accuracy |
|------|----------|----------|
| Workbench (melt) | Quick iteration | Lower (includes debugging overhead) |
| Freeze | Development profiling | Medium |
| Finalize | Production profiling | Highest (optimized code) |

For accurate performance data, use **finalized** builds.

## Profiling Workflow

### 1. Compile with Profiling
```
ec -batch -config project.ecf -target my_target -freeze -c_compile
```
Or finalize for production-accurate timing:
```
ec -batch -config project.ecf -target my_target -finalize -c_compile
```

### 2. Run the Instrumented Executable

Execute your program with a representative workload. The profiler generates a `profinfo` file in:
- Workbench/Freeze: `EIFGENs/<target>/W_CODE/profinfo`
- Finalized: `EIFGENs/<target>/F_CODE/profinfo`

### 3. Process the Profile Data

**Via EiffelStudio GUI** (recommended):
1. Open your project in EiffelStudio
2. Menu: Project > Profile
3. Profiler Wizard will guide you through conversion and analysis

**Via ec.exe -loop mode** (limited):
```
ec -loop -config project.ecf -target my_target
```
Then use `(P) Profile` menu option.

### 4. Analyze Results

The converted profile (`.pfi` file) provides:

| Metric | Description |
|--------|-------------|
| Calls | Number of times the feature was invoked |
| Self | Time spent in the feature itself |
| Descendants | Time spent in features called by this feature |
| Total | Self + Descendants |
| Percentage | % of total program execution time |

## Profiler Configuration Files

Located in: `$ISE_EIFFEL/studio/profiler/`

| File | Purpose |
|------|---------|
| `eiffel` | Internal Eiffel profiler configuration |
| `gprof` | GNU gprof external profiler configuration |
| `win32_ms` | Windows MS profiler configuration |

### Configuration File Format

```
number_of_columns: 6
index_column: 1
function_time_column: 2
descendant_time_column: 3
number_of_calls_column: 4
percentage_column: 5
function_name_column: 6
generates_leading_underscore: no
```

## Query Capabilities

The Profile menu supports filtering results:

- **By feature name**: wildcards `*` and `?` supported
- **By call count**: `calls > 1000`
- **By time**: `self > 0.1` (seconds)
- **By percentage**: `percentage > 5`

Operators: `<`, `>`, `=`, `<=`, `>=`

## Command Line Interactive Mode

When using `ec -loop`, the Profile menu (`P`) offers:
- **(G) Generate**: Convert profinfo to execution profile
- **(S) Switches**: Toggle output columns
- **(Q) Query**: Filter and search results
- **(L) Language**: Eiffel only, C only, or both

## Best Practices

1. **Profile realistic workloads** - Synthetic benchmarks may not reflect real usage
2. **Use finalized builds** - Workbench includes debugging overhead
3. **Focus on percentages first** - Optimize features consuming the most time
4. **Profile after optimization** - Verify improvements with data
5. **Keep profiles for comparison** - Rename `.pfi` files to preserve history

## Limitations

1. **GUI Required for Full Analysis**: The Profiler Wizard in EiffelStudio provides the best experience. Command-line analysis is limited.

2. **Profiling Overhead**: Instrumentation adds overhead, so absolute times may be inflated. Focus on relative percentages.

3. **Not Available for .NET**: EiffelStudio's built-in profiler doesn't work with .NET targets.

4. **Binary Format**: The `profinfo` file is binary and requires conversion before analysis.

## Alternative Approaches

For cases where the built-in profiler is insufficient:

- **valgrind/callgrind** (Linux): Use with C-compiled Eiffel, translate C names to Eiffel
- **External profilers**: Configure via custom profiler configuration files
- **Manual timing**: Use `TIME` class for targeted measurements

## Claude Code Integration

**What Claude can do**:
- Enable profiling in ECF files
- Compile with profiling enabled
- Run instrumented executables
- Discuss profiling results you share

**What requires EiffelStudio GUI**:
- Converting `profinfo` to `.pfi`
- Interactive profile analysis
- Profiler Wizard

## Sources

- [Profile Menu](https://www.eiffel.org/doc/eiffelstudio/Profile_menu)
- [How to set up a Profiler Configuration File](https://www.eiffel.org/doc/eiffelstudio/How_to_set_up_a_Profiler_Configuration_File)
- [Reuse or Generate an Execution Profile](https://www.eiffel.org/doc/eiffelstudio/Reuse_or_Generate_an_Execution_Profile)
- [Tuning a Program](https://www.eiffel.org/doc/eiffelstudio/Tuning_a_program)
- [Command Line Interactive Mode](https://www.eiffel.org/doc/eiffelstudio/Command_line_interactive_mode)
- [EC Command Line](https://dev.eiffel.com/EC_Command_Line)
