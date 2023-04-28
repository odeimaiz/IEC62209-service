# fmt: off

from math import fabs

from ..utils.common import DataSetInterface, Goodfit, ModelMetadata, SampleConfig
from .texutils import ReportStage


def write_model_metadata_tex(mm: ModelMetadata) -> str:
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|}\hline",
        r"Measurement system name & {" + mm.systemName + r"} \\\hline",
        r"Manufacturer & {" + mm.manufacturer + r"} \\\hline",
        r"Phantom type & {" + mm.phantomType + r"} \\\hline",
        r"Hardware version & {" + mm.hardwareVersion + r"} \\\hline",
        r"Software version & {" + mm.softwareVersion + r"} \\\hline",
        r"\end{tabular}"
        r"\caption{Measurement system analyzed in this report.}",
        r"\label{tab:system}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_creation_summary_tex(data: Goodfit) -> str:
    accept = "Pass" if data.accept else "Fail"
    gfval = f"{float((data.gfres[1]) * 100):.1f}"
    gfok = "Pass" if data.gfres[0] else "Fail"
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Success Criterion} & \textbf{Outcome} & \textbf{Pass / Fail} \\\hline",
        r"Acceptance of data & $\Delta SAR \in [-U, +O]$ & See Table~\ref{tab:acceptance}& \textbf{" + accept + r"} \\\hline",
        r"Model fitting & $nrmse " + ("<" if gfok else ">") + r"$ 25~\%  & " + gfval + r"~\%   & \textbf{" + gfok + r"} \\\hline",
        r"\end{tabular}",
        r"\caption{Summary of the GPI Model creation outcomes for the measurement system described in Table~\ref{tab:system}.}",
        r"\label{tab:summary}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_confirmation_summary_tex(accepted: bool, percent: float, location: float, scale: float) -> str:
    resacc = "Pass" if accepted else "Fail"
    resnorm = "Pass" if percent > 5 else "Fail"
    resloc = "Pass" if (location > -1 and location < 1) else "Fail"
    ressca = "Pass" if (scale > 0.5 and scale < 1.5) else "Fail"
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Success Criterion} & \textbf{Outcome} & \textbf{Pass / Fail} \\\hline",
        r"Acceptance of data & $\Delta SAR \in [-U, +O]$ & See Table~\ref{tab:test}& \textbf{" + resacc + r"} \\\hline",
        r"Normality & $p \ge$ 0.05 & " + f"{0.01*percent:.3f}" + r"& \textbf{" + resnorm + r"} \\\hline",
        r"Similarity & location $\in$ [-1, 1] & " + f"{location:.3f}" + r" & \textbf{" + resloc + r"} \\\cline{2-4} & scale $\in$ [0.5, 1.5] & " + f"{scale:.3f}" + r" & \textbf{" + ressca + r"} \\\hline",
        r"\end{tabular}\caption{Summary of the GPI Model confirmation outcomes for the measurement system described in Table~\ref{tab:system}.} \label{tab:summary}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_verification_summary_tex(accepted: bool) -> str:
    res = "Pass" if accepted else "Fail"
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Success Criterion} & \textbf{Outcomes} & \textbf{Pass / Fail} \\\hline",
        r"Acceptance of data & $\Delta SAR \in [-U, +O]$ & See Table~\ref{tab:test}& \textbf{" + res + r"} \\\hline",
        r"\end{tabular}\caption{Summary of the critical data space search outcomes for the measurement system described in Table~\ref{tab:system}.} \label{tab:summary}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_sample_parameters_tex(cfg: SampleConfig, stage: ReportStage) -> str:
    stagestring = "relevant" if stage == ReportStage.CREATION else ("confirmed" if stage == ReportStage.CONFIRMATION else "critically examined")
    lines = [
        r"\begin{table}[h!]\centering",
        r"\begin{tabular}{|l|c|}\hline",
        r"\textbf{Parameter} & \textbf{Value} \\\hline",
        r"Measurement area: $x$,$y$ (mm) & " + f"{cfg.measAreaX}, {cfg.measAreaY}" + r" \\\hline",
        r"Frequency range (MHz) & " + f"{cfg.fRangeMin} -- {cfg.fRangeMax}" + r"\\\hline",
        r"Size of training data & " + f"{cfg.sampleSize}" + r" \\\hline"
        r"\end{tabular}",
        r"\caption{Range of the exposure parameter space covered by the test configurations. The GPI model can therefore be considered to be " + stagestring + r" within this range.}",
        r"\label{tab:params}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_sample_acceptance_tex(accepted: bool) -> str:
    res = "Pass" if accepted else "Fail"
    lines = [
        r"\begin{table}[h]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Success Criterion} & \textbf{Outcome} & \textbf{Pass / Fail} \\\hline",
        r"Acceptance of data & $\Delta SAR \in [-U, +O]$ & See Table~\ref{tab:acceptance}& " + res + r" \\\hline",
        r"\end{tabular}\caption{Result for the acceptance criterion.}\label{tab:acceptance}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_model_fitting_tex(gfres: tuple) -> str:
    gfval = f"{float((gfres[1]) * 100):.1f}"
    gfok = "Pass" if gfres[0] else "Fail"
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Success Criterion} & \textbf{Outcome} & \textbf{Pass / Fail} \\\hline",
        r"Model fitting & $nrmse " + ("<" if gfok else ">") + r"$ 25~\%  & " + gfval + r"~\%   & \textbf{" + gfok + r"} \\\hline",
        r"\end{tabular}\caption{Quantification (normalized mean squared error) of the semi-variogram fitting quality, which affects the GPI model quality.} \label{tab:nrmse}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_normality_tex(percent: float) -> str:
    result = "Pass" if percent > 5 else "Fail"
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Specification} & \textbf{Value} & \textbf{Pass / Fail} \\\hline",
        r"Normality & $p \ge$ 5\,\% & " + f"{percent:.1f}" + r"\,\% & \textbf{" + result + r"} \\\hline",
        r"\end{tabular}\caption{Summary results of the \textit{GPI Model Confirmation} step for the measurement system described in Table~\ref{tab:system}.} \label{tab:normality}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_similarity_tex(location: float, scale: float) -> str:
    resloc = "Pass" if (location > -1 and location < 1) else "Fail"
    ressca = "Pass" if (scale > 0.5 and scale < 1.5) else "Fail"
    lines = [
        r"\begin{table}[ht]\centering",
        r"\begin{tabular}{|l|c|c|c|}\hline",
        r"\textbf{Test} & \textbf{Success Criterion} & \textbf{Outcome} & \textbf{Pass / Fail} \\\hline",
        r"Similarity & location $\in$ [-1, 1] & " + f"{location:.3f}" + r" & \textbf{" + resloc + r"} \\\cline{2-4} & scale $\in$ [0.5, 1.5] & " + f"{scale:.3f}" + r" & \textbf{" + ressca + r"} \\\hline",
        r"\end{tabular}\caption{Summary of the GPI model confirmation results for the measurement system described in Table~\ref{tab:system}.} \label{tab:qq}",
        r"\end{table}"
    ]
    return '\n'.join(lines)

def write_sample_table_tex(ds: DataSetInterface, stage: ReportStage) -> str:
    caption = "Training Data Set for 10-gram average SAR" if stage == ReportStage.CREATION else (
        "Test configurations and measurement outcomes for 10-gram average SAR" if stage == ReportStage.CONFIRMATION else
        "Critical Configurations and Measurement Outcomes for 10-gram average SAR"
    )

    lines = [
        r"\begin{center}",
        r"\begin{longtable}{|l|c|c|c|c|c|c|c|c|c|c|c|c|c|}",
        r"\caption{" + caption + r".} \label{tab:training} \\\hline",
        r"&	$P_f$	&		&	PAPR	&	BW	&	$s$	&	$\theta$	&	$x$	&	$y$	&	$SAR$	&	$u_{s}$	&	$\Delta SAR$	&	$mpe$	&	Pass \\",
        r"ant.	&	(dB)	&	Mod	&	(dB)	&	(MHz)	&	(mm)	&	(°)	&	(mm)	&	(mm)	&	(W/kg)	&	(\%)	&	(dB)	&	(dB)	&	?	\\\hline",
        r"\endfirsthead",
        r"\multicolumn{14}{c}",
        r"{{\tablename\ \thetable{} " + caption + r" -- continued from previous page}} \\\hline",
        r"&	$P_f$	&		&	PAPR	&	BW	&	$s$	&	$\theta$	&	$x$	&	$y$	&	$SAR$	&	$u_{s}$	&	$\Delta SAR$	&	$mpe$	&	Pass \\",
        r"antenna	&	(dB)	&	Mod	&	(dB)	&	(MHz)	&	(mm)	&	(°)	&	(mm)	&	(mm)	&	(W/kg)	&	(\%)	&	(dB)	&	(dB)	&	?	\\\hline",
        r"\endhead",
        r"\hline \multicolumn{14}{|r|}{{Continued on next page}} \\ \hline",
        r"\endfoot",
        r"\hline",
        r"\endlastfoot",
    ]

    cols = ["antenna", "power", "modulation", "par", "bandwidth", "distance", "angle", "x", "y", "sar10g", "u10g", "sard10g", "mpe10g"]
    mpecol = ds.headings.index("mpe10g")
    sardcol = ds.headings.index("sard10g")
    idx = []
    for col in cols:
        i = ds.headings.index(col)
        if i < 0:
            raise Exception(f"Dataset does not contain '{col}'")
        idx.append(i)
    for row in ds.rows:
        line = "{" + row[idx[0]] + "} & " + \
            f"{row[idx[1]]} & " + \
            f"{row[idx[2]]} & " + \
            f"{row[idx[3]]:.3f} & " + \
            f"{row[idx[4]]:.0f} & " + \
            f"{row[idx[5]]:.0f} & " + \
            f"{row[idx[6]]:.0f} & " + \
            f"{row[idx[7]]:.0f} & " + \
            f"{row[idx[8]]:.0f} & " + \
            f"{row[idx[9]]:.3f} & " + \
            f"{100 * row[idx[10]]:.0f} & " + \
            f"{row[idx[11]]:.1f} & " + \
            f"{row[idx[12]]:.1f} & "

        if fabs(row[sardcol]) > row[mpecol]:
            line += r"N	\\\hline"
        else:
            line += r"Y \\\hline"
        lines += [line]

    lines += [
        r"\end{longtable}",
        r"\end{center}"
    ]
    return '\n'.join(lines)

# fmt: on
