"""Plot the CEST profiles."""
import contextlib

import numpy as np
from matplotlib import gridspec as gsp
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.backends import backend_pdf

from chemex.experiments import plotting


def sigma_estimator(x):
    """Estimates standard deviation using median to exclude outliers.

    Up to 50% can be bad.

    """
    return np.median([np.median(abs(xi - np.asarray(x))) for xi in x]) * 1.1926


def compute_profiles(data_grouped, params):
    """Compute the CEST profiles used for plotting."""
    profiles = {}

    for peak, profile in data_grouped.items():
        mask_ref = profile.reference
        mask = np.logical_not(mask_ref)

        val_ref = np.mean(profile.val[mask_ref])

        b1_ppm_exp = profile.b1_offsets_to_ppm()[mask]
        mag_cal = profile.calculate_profile(params)[mask] / val_ref
        mag_exp = profile.val[mask] / val_ref
        mag_err = profile.err[mask] / np.absolute(val_ref)
        filtered = profile.mask[mask]

        b1_offsets_min, b1_offsets_max = plotting.set_lim(
            profile.b1_offsets[mask], 0.02
        )
        b1_offsets = np.linspace(b1_offsets_min, b1_offsets_max, 500)

        b1_ppm_fit = profile.b1_offsets_to_ppm(b1_offsets)
        mag_fit = profile.calculate_profile(params, b1_offsets) / val_ref

        cs_a = params.get(profile.map_names.get("cs_i_a"))
        cs_b = params.get(profile.map_names.get("cs_i_b"))
        cs_c = params.get(profile.map_names.get("cs_i_c"))
        cs_d = params.get(profile.map_names.get("cs_i_d"))

        profiles[peak] = (
            b1_ppm_exp,
            mag_cal,
            mag_exp,
            mag_err,
            b1_ppm_fit,
            mag_fit,
            cs_a,
            cs_b,
            cs_c,
            cs_d,
            filtered,
        )

    return profiles


def write_profile_fit(name, b1_ppm_fit, mag_fit, file_):
    """Write the fitted CEST profile."""

    file_.write("[{}]\n".format(name.upper()))

    file_.write("# {:>17s}   {:>17s}\n".format("OFFSET", "INTENSITY"))

    for b1_ppm_cal, mag_cal in zip(b1_ppm_fit, mag_fit):
        file_.write(f"  {b1_ppm_cal:17.8e} = {mag_cal:17.8e}\n")

    file_.write("\n")


def write_profile_exp(name, b1_ppm, mag_exp, mag_err, file_):
    """Write the experimental CEST profile."""

    file_.write("[{}]\n".format(name.upper()))

    file_.write(
        "# {:>17s}   {:>17s} {:>17s}\n".format("OFFSET", "INTENSITY", "UNCERTAINTY")
    )

    for b1_ppm_, mag_exp_, mag_err_ in zip(b1_ppm, mag_exp, mag_err):
        file_.write(f"  {b1_ppm_:17.8e} = {mag_exp_:17.8e} {mag_err_:17.8e}\n")

    file_.write("\n")


def plot_data(data, params, output_dir):
    """Write experimental and fitted data to a file and plot the CEST profiles.

    - *.exp: contains the experimental data
    - *.fit: contains the fitted data
    - *.pdf: contains the plot of experimental and fitted data

    """
    datasets = dict()

    for data_point in data:
        experiment_name = data_point.experiment_name
        datasets.setdefault(experiment_name, []).append(data_point)

    for experiment_name, dataset in datasets.items():
        basename = output_dir / experiment_name
        name_pdf = basename.with_suffix(".pdf")
        name_fit = basename.with_suffix(".fit")
        name_exp = basename.with_suffix(".exp")

        print((f"  * {name_pdf} [.fit, .exp]"))

        data_grouped = plotting.group_data(dataset)

        profiles = compute_profiles(data_grouped, params)

        with contextlib.ExitStack() as stack:
            file_pdf = stack.enter_context(backend_pdf.PdfPages(name_pdf))
            file_fit = stack.enter_context(name_fit.open("w"))
            file_exp = stack.enter_context(name_exp.open("w"))

            for peak in sorted(profiles):
                (
                    b1_ppm,
                    mag_cal,
                    mag_exp,
                    mag_err,
                    b1_ppm_fit,
                    mag_fit,
                    cs_a,
                    cs_b,
                    cs_c,
                    cs_d,
                    filtered,
                ) = profiles[peak]

                write_profile_fit(peak.assignment, b1_ppm_fit, mag_fit, file_fit)
                write_profile_exp(peak.assignment, b1_ppm, mag_exp, mag_err, file_exp)

                # Matplotlib #
                grid_spec = gsp.GridSpec(2, 1, height_ratios=[1, 4])

                ax1 = plt.subplot(grid_spec[0])
                ax2 = plt.subplot(grid_spec[1])

                cs_colors = list(
                    zip(
                        (cs_a, cs_b, cs_c, cs_d),
                        ("Blue", "Red", "Orange", "Deep Orange"),
                    )
                )

                for ax_ in (ax1, ax2):
                    for a_cs, color in cs_colors:
                        if a_cs is not None:
                            ax_.axvline(
                                a_cs.value,
                                color=plotting.PALETTE[color]["100"],
                                linestyle="-",
                                linewidth=1.0,
                                zorder=-100,
                            )

                    ax_.axhline(
                        0, color=plotting.PALETTE["Black"]["Text"], linewidth=0.5
                    )

                ########################

                ax2.plot(
                    b1_ppm_fit,
                    mag_fit,
                    linestyle="-",
                    color=plotting.PALETTE["Grey"]["700"],
                    zorder=2,
                )

                ax2.errorbar(
                    b1_ppm[filtered],
                    mag_exp[filtered],
                    mag_err[filtered],
                    fmt="o",
                    markeredgecolor=plotting.PALETTE["Red"]["500"],
                    ecolor=plotting.PALETTE["Red"]["500"],
                    markerfacecolor="None",
                    zorder=3,
                )

                unfiltered = np.logical_not(filtered)

                ax2.errorbar(
                    b1_ppm[unfiltered],
                    mag_exp[unfiltered],
                    mag_err[unfiltered],
                    fmt="o",
                    markeredgecolor=plotting.PALETTE["Red"]["100"],
                    ecolor=plotting.PALETTE["Red"]["100"],
                    markerfacecolor="None",
                    zorder=3,
                )

                xmin, xmax = plotting.set_lim(b1_ppm_fit, 0.05)
                mags = list(mag_exp) + list(mag_fit)
                ymin, ymax = plotting.set_lim(mags, 0.10)

                ax2.set_xlim(xmin, xmax)
                ax2.set_ylim(ymin, ymax)

                ax2.invert_xaxis()

                ax2.xaxis.set_major_locator(ticker.MaxNLocator(9))
                # ax2.yaxis.set_major_locator(ticker.MaxNLocator(6))

                ax2.xaxis.grid(False)

                ax2.set_xlabel(r"$\mathregular{B_1 \ position \ (ppm)}$")
                ax2.set_ylabel(r"$\mathregular{I/I_0}$")

                ########################

                deltas = np.asarray(mag_exp) - np.asarray(mag_cal)
                sigma = sigma_estimator(deltas)

                ax1.fill(
                    (xmin, xmin, xmax, xmax),
                    1.0 * sigma * np.asarray([-1.0, 1.0, 1.0, -1.0]),
                    fc=plotting.PALETTE["Black"]["Dividers"],
                    ec="none",
                )

                ax1.fill(
                    (xmin, xmin, xmax, xmax),
                    2.0 * sigma * np.asarray([-1.0, 1.0, 1.0, -1.0]),
                    fc=plotting.PALETTE["Black"]["Dividers"],
                    ec="none",
                )

                ax1.errorbar(
                    b1_ppm[filtered],
                    deltas[filtered],
                    mag_err[filtered],
                    fmt="o",
                    markeredgecolor=plotting.PALETTE["Red"]["500"],
                    ecolor=plotting.PALETTE["Red"]["500"],
                    markerfacecolor="None",
                    zorder=100,
                )

                ax1.errorbar(
                    b1_ppm[unfiltered],
                    deltas[unfiltered],
                    mag_err[unfiltered],
                    fmt="o",
                    markeredgecolor=plotting.PALETTE["Red"]["100"],
                    ecolor=plotting.PALETTE["Red"]["100"],
                    markerfacecolor="None",
                    zorder=100,
                )

                rmin, rmax = plotting.set_lim(deltas, 0.1)
                rmin = min([-3 * sigma, rmin - max(mag_err)])
                rmax = max([+3 * sigma, rmax + max(mag_err)])

                ax1.set_xlim(xmin, xmax)
                ax1.set_ylim(rmin, rmax)

                ax1.invert_xaxis()

                ax1.xaxis.set_major_locator(ticker.MaxNLocator(9))
                ax1.yaxis.set_major_locator(ticker.MaxNLocator(4))

                ax1.xaxis.set_major_formatter(ticker.NullFormatter())

                ax1.xaxis.grid(False)
                ax1.yaxis.grid(False)

                ax1.ticklabel_format(style="sci", scilimits=(0, 0), axis="y")

                ax1.set_title("{:s}".format(peak.assignment.upper()))
                ax1.set_ylabel("Residual")

                ########################

                for ax in (ax1, ax2):
                    ax.yaxis.set_ticks_position("left")
                    ax.xaxis.set_ticks_position("bottom")

                ########################

                file_pdf.savefig()
                plt.close()

                ########################

    return
