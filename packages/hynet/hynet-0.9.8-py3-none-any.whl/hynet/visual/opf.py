"""
Visualization functionality for optimal power flow results.
"""

import logging

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from hynet.types_ import SolverType

_log = logging.getLogger(__name__)


def _check_data_availability(result):
    """Check availability of OPF result data."""
    if result.empty:
        raise RuntimeError("The OPF result is empty.")
    if not result.is_physical:
        if result.solver.type == SolverType.QCQP:
            remark = "solver issue"
        else:
            remark = "inexact relaxation or solver issue"
        _log.warning("The OPF result does not satisfy the power "
                     "balance ({0:s}).".format(remark))


def _set_id_labels(axis, index):
    """
    Relabel the one-based linear ticks with the IDs in ``index``.
    """
    axis.set_xticklabels(
        ['' if not (i.is_integer() and 1 <= i <= len(index))
         else str(index[int(i - 1)]) for i in axis.get_xticks()])


def show_lmp_profile(result, id_label=False):
    """
    Show the LMP profile or power balance dual variables for an OPF result.

    For a consistent appearance in case of nonconsecutive or custom IDs,
    **the buses are numbered consecutively starting from 1 for the
    labeling of the x-axis**. To enforce labeling of the ticks with the
    IDs, set ``id_label=True``.

    Parameters
    ----------
    result : OPFResult
        Optimal power flow result that shall be visualized.
    id_label : bool, optional
        If True, the linear ticks are relabeled with the bus IDs.
    """
    _check_data_availability(result)
    if result.num_buses < 2:
        raise RuntimeError("LMP profile visualization is only available "
                           "for two or more buses.")
    if result.solver.type == SolverType.QCQP:
        # Zero duality gap is not ensured...
        title = "KKT multipliers for {:s} power balance"
    elif not result.is_physical:
        # Relaxation is not exact...
        title = "Dual variables for {:s} power balance"
    else:
        title = "LMP profile for {:s} power"

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(2, 1, 1)
    linear_index = 1 + np.arange(result.num_buses)
    ax.plot(linear_index, result.bus['dv_bal_p'].values,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, result.bus.index)
    ax.set_title(title.format('active'))
    ax.set_ylabel('$/MWh')
    ax.set_xlabel('Bus ' + ('ID' if id_label else 'Index'))
    ax = fig.add_subplot(2, 1, 2)
    ax.plot(linear_index, result.bus['dv_bal_q'].values,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, result.bus.index)
    ax.set_title(title.format('reactive'))
    ax.set_ylabel('$/Mvarh')
    ax.set_xlabel('Bus ' + ('ID' if id_label else 'Index'))
    fig.tight_layout()
    fig.show()
    return fig


def show_voltage_profile(result, id_label=False):
    """
    Show the voltage profile for an OPF result.

    For a consistent appearance in case of nonconsecutive or custom IDs,
    **the buses are numbered consecutively starting from 1 for the
    labeling of the x-axis**. To enforce labeling of the ticks with the
    IDs, set ``id_label=True``.

    Parameters
    ----------
    result : OPFResult
        Optimal power flow result that shall be visualized.
    id_label : bool, optional
        If True, the linear ticks are relabeled with the bus IDs.
    """
    _check_data_availability(result)
    if result.num_buses < 2:
        raise RuntimeError("Voltage profile visualization is only "
                           "available for two or more buses.")
    fig = plt.figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)
    linear_index = 1 + np.arange(result.num_buses)
    v_min = result.scenario.bus.loc[result.bus.index, 'v_min']
    ax.plot(linear_index, v_min.values,
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    v_max = result.scenario.bus.loc[result.bus.index, 'v_max']
    ax.plot(linear_index, v_max.values,
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, result.bus['v'].abs().values,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, result.bus.index)
    ax.set_title("Voltage profile")
    ax.set_ylabel('p.u.')
    ax.set_xlabel('Bus ' + ('ID' if id_label else 'Index'))
    fig.tight_layout()
    fig.show()
    return fig


def show_branch_flow_profile(result, id_label=False):
    """
    Show the branch flow profile for an OPF result.

    For a consistent appearance in case of nonconsecutive or custom IDs,
    **the branches are numbered consecutively starting from 1 for the
    labeling of the x-axis**. To enforce labeling of the ticks with the
    IDs, set ``id_label=True``.

    Parameters
    ----------
    result : OPFResult
        Optimal power flow result that shall be visualized.
    id_label : bool, optional
        If True, the linear ticks are relabeled with the branch IDs.
    """
    _check_data_availability(result)
    if result.num_branches < 2:
        raise RuntimeError("Branch flow profile visualization is only "
                           "available for two or more branches.")
    fig = plt.figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)
    linear_index = 1 + np.arange(result.num_branches)
    ax.plot(linear_index, result.branch['effective_rating'].values,
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index,
            result.branch[['s_src', 's_dst']].abs().max(axis=1).values,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, result.branch.index)
    ax.set_title("Branch flow profile")
    ax.set_ylabel('MVA for AC / MW for DC')
    ax.set_xlabel('Branch ' + ('ID' if id_label else 'Index'))
    fig.tight_layout()
    fig.show()
    return fig


def show_ampacity_dual_profile(result, id_label=False):
    """
    Show the ampacity dual variable profile for an OPF result.

    For a consistent appearance in case of nonconsecutive or custom IDs,
    **the branches are numbered consecutively starting from 1 for the
    labeling of the x-axis**. To enforce labeling of the ticks with the
    IDs, set ``id_label=True``.

    Parameters
    ----------
    result : OPFResult
        Optimal power flow result that shall be visualized.
    id_label : bool, optional
        If True, the linear ticks are relabeled with the branch IDs.
    """
    _check_data_availability(result)
    if result.num_branches < 2:
        raise RuntimeError("Ampacity dual variable profile visualization "
                           "is only available for two or more branches.")
    dv_ampacity = result.branch[['dv_i_max_src',
                                 'dv_i_max_dst']].sum(axis=1).values
    fig = plt.figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)
    linear_index = 1 + np.arange(result.num_branches)
    ax.plot(linear_index, dv_ampacity,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, result.branch.index)
    ax.set_title("Ampacity dual variable profile")
    ax.set_ylabel('Dual Variable')
    ax.set_xlabel('Branch ' + ('ID' if id_label else 'Index'))
    fig.tight_layout()
    fig.show()
    return fig


def show_converter_flow_profile(result, id_label=False):
    """
    Show the converter active power flow profile for an OPF result.

    For a consistent appearance in case of nonconsecutive or custom IDs,
    **the converters are numbered consecutively starting from 1 for the
    labeling of the x-axis**. To enforce labeling of the ticks with the
    IDs, set ``id_label=True``.

    Parameters
    ----------
    result : OPFResult
        Optimal power flow result that shall be visualized.
    id_label : bool, optional
        If True, the linear ticks are relabeled with the converter IDs.
    """
    _check_data_availability(result)
    if result.num_converters < 2:
        raise RuntimeError("Converter flow profile visualization is only "
                           "available for two or more converters.")
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(2, 1, 1)
    index = result.converter.index
    linear_index = 1 + np.arange(result.num_converters)
    cap_src = result.scenario.converter.loc[index, 'cap_src']
    ax.plot(linear_index, [x.p_min for x in cap_src],
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, [x.p_max for x in cap_src],
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, result.converter['p_src'].values,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, index)
    ax.set_title("Converter flow profile at the source terminal")
    ax.set_ylabel('MW')
    ax.set_xlabel('Converter ' + ('ID' if id_label else 'Index'))
    ax = fig.add_subplot(2, 1, 2)
    cap_dst = result.scenario.converter.loc[index, 'cap_dst']
    ax.plot(linear_index, [x.p_min for x in cap_dst],
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, [x.p_max for x in cap_dst],
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, result.converter['p_dst'].values,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, index)
    ax.set_title("Converter flow profile at the destination terminal")
    ax.set_ylabel('MW')
    ax.set_xlabel('Converter ' + ('ID' if id_label else 'Index'))
    fig.tight_layout()
    fig.show()
    return fig


def show_dispatch_profile(result, id_label=False):
    """
    Show the active power injector dispatch profile for an OPF result.

    For a consistent appearance in case of nonconsecutive or custom IDs,
    **the injectors are numbered consecutively starting from 1 for the
    labeling of the x-axis**. To enforce labeling of the ticks with the
    IDs, set ``id_label=True``.

    Parameters
    ----------
    result : OPFResult
        Optimal power flow result that shall be visualized.
    id_label : bool, optional
        If True, the linear ticks are relabeled with the injector IDs.
    """
    _check_data_availability(result)
    if result.num_injectors < 2:
        raise RuntimeError("Injector dispatch visualization is only "
                           "available for two or more injectors.")
    fig = plt.figure(figsize=(10, 3))
    ax = fig.add_subplot(1, 1, 1)
    linear_index = 1 + np.arange(result.num_injectors)
    cap = result.scenario.injector.loc[result.injector.index, 'cap']
    ax.plot(linear_index, [x.p_min for x in cap],
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, [x.p_max for x in cap],
            color='xkcd:light red', linestyle='--', linewidth=0.5)
    ax.plot(linear_index, result.injector['s'].values.real,
            color='xkcd:sea blue', linestyle='-', linewidth=1)
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if id_label:
        _set_id_labels(ax, result.injector.index)
    ax.set_title("Active power injector dispatch profile")
    ax.set_ylabel('MW')
    ax.set_xlabel('Injector ' + ('ID' if id_label else 'Index'))
    fig.tight_layout()
    fig.show()
    return fig
