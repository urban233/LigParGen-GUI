import logging
from typing import Optional
from PyQt6 import QtCore, QtGui, QtWidgets
from ligpargen_gui.gui.custom_widgets import accordion, custom_button, custom_label, toggle_button
from ligpargen_gui.model.preference import model_definitions
from ligpargen_gui.model.util.gui_style import icons
from ligpargen_gui.gui.main.forms.auto import auto_main_frame
from ligpargen_gui.model.util import exception, safeguard
from ligpargen_gui.model.custom_logging import default_logging

logger = default_logging.setup_logger(__file__)

__docformat__ = "google"


class MainFrame(QtWidgets.QMainWindow):
  """Main form."""

  # <editor-fold desc="Class attributes">
  dialogClosed = QtCore.pyqtSignal(tuple)
  """A signal indicating that the dialog is closed."""
  # </editor-fold>

  def __init__(self) -> None:
    """Constructor."""
    super().__init__()
    # build ui object
    self.ui = auto_main_frame.Ui_MainWindow()
    self.ui.setupUi(self)

    # <editor-fold desc="Menu bar">
    menu_bar = self.menuBar()
    self.application_menu = menu_bar.addMenu('Application')
    self.help_menu = menu_bar.addMenu('Help')
    self.exit_action = QtGui.QAction('Exit', self)
    self.docs_action = QtGui.QAction('Documentation', self)
    self.open_logs_folder_action = QtGui.QAction('Open logs folder', self)
    self.clear_all_logs_action = QtGui.QAction('Clear all logs', self)
    self.about_action = QtGui.QAction('About', self)
    self.application_menu.addSeparator()
    self.application_menu.addAction(self.exit_action)
    self.help_menu.addAction(self.docs_action)
    self.help_menu.addAction(self.open_logs_folder_action)
    self.help_menu.addAction(self.clear_all_logs_action)
    self.help_menu.addSeparator()
    self.help_menu.addAction(self.about_action)
    # </editor-fold>

    shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(8)
    shadow_effect.setOffset(3, 3)
    shadow_effect.setColor(QtGui.QColor(0, 0, 0, 15))
    self.ui.main_content_frame.setGraphicsEffect(shadow_effect)
    self.ui.main_content_frame.setStyleSheet(
      """QFrame#main_content_frame {
        border: 1px solid white;
        background: white;
        margin: 5px;
        border-radius: 10px;
      }
      """
    )
    # <editor-fold desc="Structure input">
    self.structure_input_layout = QtWidgets.QVBoxLayout()
    self.structure_input_layout.setContentsMargins(0, 0, 0, 5)
    self.structure_input_layout.setSpacing(4)
    self.structure_input_sub_layout = QtWidgets.QGridLayout()
    self.structure_input_sub_layout.setContentsMargins(0, 0, 0, 0)
    self.lbl_structure_input = QtWidgets.QLabel("Input structures")
    self.txt_structure_input = QtWidgets.QLineEdit()
    self.btn_structure_input = QtWidgets.QPushButton("...")

    self.structure_input_menu = custom_button.PersistentQMenu()
    self.action_structure_input_pdb = QtGui.QAction("PDB files", self)
    self.action_structure_input_smiles = QtGui.QAction("SMILES text file", self)
    self.structure_input_menu.addAction(self.action_structure_input_pdb)
    self.structure_input_menu.addAction(self.action_structure_input_smiles)

    icons.set_icon(self.btn_structure_input, model_definitions.IconsEnum.OPEN)
    self.btn_structure_input.setStyleSheet(
      """
      QPushButton {
          background-color: rgba(220, 219, 227, 0.01);
          border: none;
          border-radius: 4px;
          min-width: 36px;
          max-width: 36px;
          min-height: 36px;
          max-height: 36px;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          border: none;
          min-width: 40px;
          max-width: 40px;
          min-height: 40px;
          max-height: 40px;
      }
      """
    )
    #self.lbl_structure_input_status = QtWidgets.QLabel("")
    #self.lbl_structure_input_status.setStyleSheet("""color: #ba1a1a; font-size: 11px; padding:0px;""")
    self.structure_input_layout.addWidget(self.lbl_structure_input)
    self.structure_input_sub_layout.addWidget(self.txt_structure_input, 0, 0)
    self.structure_input_sub_layout.addWidget(self.btn_structure_input, 0, 1)
    #self.structure_input_sub_layout.addWidget(self.lbl_structure_input_status, 1, 0)
    self.structure_input_layout.addLayout(self.structure_input_sub_layout)
    # </editor-fold>

    # <editor-fold desc="Accordion widget">
    # <editor-fold desc="Options">
    self.container_options = QtWidgets.QWidget()
    self.container_options_layout = QtWidgets.QVBoxLayout()
    self.mol_optimization_iter_layout = QtWidgets.QHBoxLayout()
    self.lbl_mol_optimization_iter = QtWidgets.QLabel("Select molecule optimization iterations")
    self.cbox_mol_optimization_iter = QtWidgets.QComboBox()
    self.mol_optimization_iter_layout.addWidget(self.lbl_mol_optimization_iter)
    self.mol_optimization_iter_layout.addStretch()
    self.mol_optimization_iter_layout.addWidget(self.cbox_mol_optimization_iter)
    self.container_options_layout.addLayout(self.mol_optimization_iter_layout)
    self.charge_model_layout = QtWidgets.QHBoxLayout()
    self.lbl_charge_model = QtWidgets.QLabel("Select charge model")
    self.cbox_charge_model = QtWidgets.QComboBox()
    self.charge_model_layout.addWidget(self.lbl_charge_model)
    self.charge_model_layout.addStretch()
    self.charge_model_layout.addWidget(self.cbox_charge_model)
    self.container_options_layout.addLayout(self.charge_model_layout)
    self.molecule_charge_layout = QtWidgets.QHBoxLayout()
    self.lbl_molecule_charge = QtWidgets.QLabel("Select molecule charge")
    self.cbox_molecule_charge = QtWidgets.QComboBox()
    self.molecule_charge_layout.addWidget(self.lbl_molecule_charge)
    self.molecule_charge_layout.addStretch()
    self.molecule_charge_layout.addWidget(self.cbox_molecule_charge)
    self.container_options_layout.addLayout(self.molecule_charge_layout)
    self.timeout_layout = QtWidgets.QHBoxLayout()
    self.lbl_timeout = QtWidgets.QLabel("Set LigParGen timeout (in secs)")
    self.txt_timeout = QtWidgets.QLineEdit()
    self.txt_timeout.setPlaceholderText("60")
    self.txt_timeout.setStyleSheet("""QLineEdit {min-width: 45px; max-width: 45px; color: #000000; border-color: #DCDBE3;}""")
    self.timeout_layout.addWidget(self.lbl_timeout)
    self.timeout_layout.addStretch()
    self.timeout_layout.addWidget(self.txt_timeout)
    self.container_options_layout.addLayout(self.timeout_layout)
    self.container_options.setLayout(self.container_options_layout)

    self.accordion_section_options = accordion.AccordionSection(
      "Options", self.container_options
    )
    # </editor-fold>

    # <editor-fold desc="Results">
    """Results generated by ligpargen (x is a placeholder for a molecule name)
    x.charmm.pdb
    x.charmm.prm
    x.charmm.rtf
    x.desmond.cms
    x.gmx.gro
    x.gmx.itp
    x.lammps.lmp
    x.openmm.pdb
    x.openmm.xml
    x.pqr
    x.q.lib
    x.q.pdb
    x.q.prm
    x.tinker.key
    x.tinker.xyz
    x.xplor.param
    x.xplor.top
    x.z
    x-debug.pdb
    """
    self.container_results = QtWidgets.QWidget()
    self.container_results_layout = QtWidgets.QVBoxLayout()
    self.lbl_output_files = QtWidgets.QLabel("Choose output files")
    self.container_results_all = QtWidgets.QHBoxLayout()
    self.lbl_select_all = QtWidgets.QLabel("Generate all output files")
    self.tg_select_all = toggle_button.ToggleWidget()
    self.container_results_all.addWidget(self.lbl_select_all)
    self.container_results_all.addStretch()
    self.container_results_all.addWidget(self.tg_select_all)
    self.container_results_layout_first_row = QtWidgets.QHBoxLayout()
    self.container_results_layout_second_row = QtWidgets.QHBoxLayout()
    self.container_results_layout_third_row = QtWidgets.QHBoxLayout()

    # <editor-fold desc="APBS">
    self.apbs_layout = QtWidgets.QVBoxLayout()
    self.apbs_menu = custom_button.PersistentQMenu()
    self.action_apbs_pqr = QtGui.QAction(".pqr", self)
    self.action_apbs_pqr.setCheckable(True)
    self.apbs_menu.addAction(self.action_apbs_pqr)
    self.btn_apbs = custom_button.DropDownButton("APBS", self.apbs_menu)
    self.action_apbs_pqr.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_apbs, checked)
    )
    self.apbs_layout.addWidget(self.btn_apbs)
    self.container_results_layout_first_row.addLayout(self.apbs_layout)
    # </editor-fold>

    # <editor-fold desc="CHARMM">
    self.charmm_layout = QtWidgets.QVBoxLayout()
    self.charmm_menu = custom_button.PersistentQMenu()
    self.action_charmm_pdb = QtGui.QAction(".pdb", self)
    self.action_charmm_pdb.setCheckable(True)
    self.action_charmm_prm = QtGui.QAction(".prm", self)
    self.action_charmm_prm.setCheckable(True)
    self.action_charmm_rtf = QtGui.QAction(".rtf", self)
    self.action_charmm_rtf.setCheckable(True)
    self.charmm_menu.addAction(self.action_charmm_pdb)
    self.charmm_menu.addAction(self.action_charmm_prm)
    self.charmm_menu.addAction(self.action_charmm_rtf)
    self.btn_charmm = custom_button.DropDownButton("CHARMM", self.charmm_menu)
    self.action_charmm_pdb.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_charmm, checked)
    )
    self.action_charmm_prm.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_charmm, checked)
    )
    self.action_charmm_rtf.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_charmm, checked)
    )
    self.charmm_layout.addWidget(self.btn_charmm)
    self.container_results_layout_first_row.addLayout(self.charmm_layout)
    # </editor-fold>

    # <editor-fold desc="Desmond">
    self.desmond_layout = QtWidgets.QVBoxLayout()
    self.desmond_menu = custom_button.PersistentQMenu()
    self.action_desmond_cms = QtGui.QAction(".cms", self)
    self.action_desmond_cms.setCheckable(True)
    self.desmond_menu.addAction(self.action_desmond_cms)
    self.btn_desmond = custom_button.DropDownButton("Desmond", self.desmond_menu)
    self.desmond_layout.addWidget(self.btn_desmond)
    self.action_desmond_cms.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_desmond, checked)
    )
    self.container_results_layout_first_row.addLayout(self.desmond_layout)
    # </editor-fold>

    # <editor-fold desc="Gromacs">
    self.gromacs_layout = QtWidgets.QVBoxLayout()
    self.gromacs_menu = custom_button.PersistentQMenu()
    self.action_gromacs_gro = QtGui.QAction(".gro", self)
    self.action_gromacs_gro.setCheckable(True)
    self.action_gromacs_itp = QtGui.QAction(".itp", self)
    self.action_gromacs_itp.setCheckable(True)
    self.gromacs_menu.addAction(self.action_gromacs_gro)
    self.gromacs_menu.addAction(self.action_gromacs_itp)
    self.btn_gromacs = custom_button.DropDownButton("GROMACS", self.gromacs_menu)
    self.action_gromacs_gro.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_gromacs, checked)
    )
    self.action_gromacs_itp.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_gromacs, checked)
    )
    self.gromacs_layout.addWidget(self.btn_gromacs)
    self.container_results_layout_second_row.addLayout(self.gromacs_layout)
    # </editor-fold>

    # <editor-fold desc="LAMMPS">
    self.lammps_layout = QtWidgets.QVBoxLayout()
    self.lammps_menu = custom_button.PersistentQMenu()
    self.action_lammps_lmp = QtGui.QAction(".lmp", self)
    self.action_lammps_lmp.setCheckable(True)
    self.lammps_menu.addAction(self.action_lammps_lmp)
    self.btn_lammps = custom_button.DropDownButton("LAMMPS", self.lammps_menu)
    self.action_lammps_lmp.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_lammps, checked)
    )
    self.lammps_layout.addWidget(self.btn_lammps)
    self.container_results_layout_second_row.addLayout(self.lammps_layout)
    # </editor-fold>

    # <editor-fold desc="OpenMM">
    self.openmm_layout = QtWidgets.QVBoxLayout()
    self.openmm_menu = custom_button.PersistentQMenu()
    self.action_openmm_pdb = QtGui.QAction(".pdb", self)
    self.action_openmm_pdb.setCheckable(True)
    self.action_openmm_xml = QtGui.QAction(".xml", self)
    self.action_openmm_xml.setCheckable(True)
    self.openmm_menu.addAction(self.action_openmm_pdb)
    self.openmm_menu.addAction(self.action_openmm_xml)
    self.btn_openmm = custom_button.DropDownButton("OpenMM", self.openmm_menu)
    self.action_openmm_pdb.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_openmm, checked)
    )
    self.action_openmm_xml.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_openmm, checked)
    )
    self.openmm_layout.addWidget(self.btn_openmm)
    self.container_results_layout_second_row.addLayout(self.openmm_layout)
    # </editor-fold>

    # <editor-fold desc="Q">
    self.q_layout = QtWidgets.QVBoxLayout()
    self.q_menu = custom_button.PersistentQMenu()
    self.action_q_lib = QtGui.QAction(".lib", self)
    self.action_q_lib.setCheckable(True)
    self.action_q_pdb = QtGui.QAction(".pdb", self)
    self.action_q_pdb.setCheckable(True)
    self.action_q_prm = QtGui.QAction(".prm", self)
    self.action_q_prm.setCheckable(True)
    self.q_menu.addAction(self.action_q_lib)
    self.q_menu.addAction(self.action_q_pdb)
    self.q_menu.addAction(self.action_q_prm)
    self.btn_q = custom_button.DropDownButton("Q", self.q_menu)
    self.action_q_lib.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_q, checked)
    )
    self.action_q_pdb.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_q, checked)
    )
    self.action_q_prm.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_q, checked)
    )
    self.q_layout.addWidget(self.btn_q)
    self.container_results_layout_third_row.addLayout(self.q_layout)
    # </editor-fold>

    # <editor-fold desc="Tinker">
    self.tinker_layout = QtWidgets.QVBoxLayout()
    self.tinker_menu = custom_button.PersistentQMenu()
    self.action_tinker_xyz = QtGui.QAction(".xyz", self)
    self.action_tinker_xyz.setCheckable(True)
    self.action_tinker_key = QtGui.QAction(".key", self)
    self.action_tinker_key.setCheckable(True)
    self.tinker_menu.addAction(self.action_tinker_xyz)
    self.tinker_menu.addAction(self.action_tinker_key)
    self.btn_tinker = custom_button.DropDownButton("TINKER", self.tinker_menu)
    self.action_tinker_xyz.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_tinker, checked)
    )
    self.action_tinker_key.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_tinker, checked)
    )
    self.tinker_layout.addWidget(self.btn_tinker)
    self.container_results_layout_third_row.addLayout(self.tinker_layout)
    # </editor-fold>

    # <editor-fold desc="X-PLOR">
    self.xplor_layout = QtWidgets.QVBoxLayout()
    self.xplor_menu = custom_button.PersistentQMenu()
    self.action_xplor_param = QtGui.QAction(".param", self)
    self.action_xplor_param.setCheckable(True)
    self.action_xplor_top = QtGui.QAction(".top", self)
    self.action_xplor_top.setCheckable(True)
    self.xplor_menu.addAction(self.action_xplor_param)
    self.xplor_menu.addAction(self.action_xplor_top)
    self.btn_xplor = custom_button.DropDownButton("X-PLOR", self.xplor_menu)
    self.action_xplor_param.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_xplor, checked)
    )
    self.action_xplor_top.toggled.connect(
      lambda checked: custom_button.DropDownButton.update_button_color(self.btn_xplor, checked)
    )
    self.xplor_layout.addWidget(self.btn_xplor)
    self.container_results_layout_third_row.addLayout(self.xplor_layout)
    # </editor-fold>
    # </editor-fold>

    self.container_results_layout_first_row.addStretch()
    self.container_results_layout_second_row.addStretch()
    self.container_results_layout_third_row.addStretch()

    # <editor-fold desc="Output directory">
    self.output_directory_layout = QtWidgets.QVBoxLayout()
    self.output_directory_layout.setContentsMargins(0, 13, 0, 0)
    self.output_directory_layout.setSpacing(4)
    self.output_directory_sub_layout = QtWidgets.QGridLayout()
    self.output_directory_sub_layout.setContentsMargins(0, 0, 0, 0)
    self.lbl_output_directory = QtWidgets.QLabel("Output folder for results")
    self.txt_output_directory = QtWidgets.QLineEdit()
    self.btn_output_directory = QtWidgets.QPushButton("...")
    icons.set_icon(self.btn_output_directory, model_definitions.IconsEnum.OPEN)
    self.btn_output_directory.setStyleSheet(
      """
      QPushButton {
          background-color: rgba(220, 219, 227, 0.01);
          border: none;
          border-radius: 4px;
          min-width: 36px;
          max-width: 36px;
          min-height: 36px;
          max-height: 36px;
      }
      QPushButton::hover {
          background-color: rgba(220, 219, 227, 0.5);
          border: none;
          min-width: 40px;
          max-width: 40px;
          min-height: 40px;
          max-height: 40px;
      }
      """
    )
    #self.lbl_output_directory_status = QtWidgets.QLabel("")
    # self.lbl_output_directory_status.setStyleSheet(
    #   """color: #ba1a1a; font-size: 11px; margin-top: 0px; margin-bottom: 15px; padding:0px;""")
    self.output_directory_layout.addWidget(self.lbl_output_directory)
    self.output_directory_sub_layout.addWidget(self.txt_output_directory, 0, 0)
    self.output_directory_sub_layout.addWidget(self.btn_output_directory, 0, 1)
    #self.output_directory_sub_layout.addWidget(self.lbl_output_directory_status, 1, 0)
    self.output_directory_layout.addLayout(self.output_directory_sub_layout)
    # </editor-fold>

    self.container_results_layout.addLayout(self.container_results_all)
    self.container_results_layout.addWidget(self.lbl_output_files)
    self.container_results_layout.addLayout(self.container_results_layout_first_row)
    self.container_results_layout.addLayout(self.container_results_layout_second_row)
    self.container_results_layout.addLayout(self.container_results_layout_third_row)
    self.container_results_layout.addLayout(self.output_directory_layout)
    self.accordion_section_results = accordion.AccordionSection(
      "Results", self.container_results
    )
    self.container_results.setLayout(self.container_results_layout)

    self.accordion = accordion.AccordionWidget(
      [self.accordion_section_options, self.accordion_section_results]
    )

    self.ui.main_frame_layout.addLayout(self.structure_input_layout)
    self.ui.main_frame_layout.addWidget(self.accordion)
    # </editor-fold>

    # <editor-fold desc="Start job button">
    self.start_job_layout = QtWidgets.QHBoxLayout()
    self.btn_start_job = QtWidgets.QPushButton("Start job")
    self.btn_start_job.setStyleSheet(
      """
      QPushButton {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }
    
    QPushButton:disabled {
        background-color: #fff;
        color: #B0B0B0;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 1px;
        border-radius: 4px;
        border-color: #DCDCDC;
        padding: 2px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }
    
    QPushButton::pressed {
        background-color: #fff;
        color: black;
        font-family: "Segoe UI";
        font-size: 12px;
        border: solid;
        border-width: 2px;
        border-radius: 4px;
        border-color: #367AF6;
        padding: 0px;
        min-width: 65px;
        max-width: 65px;
        min-height: 15px;
    }
      """
    )
    self.start_job_layout.addStretch()
    self.start_job_layout.addWidget(self.btn_start_job)
    # </editor-fold>

    self.lbl_error_message = custom_label.ErrorMessageLabel(self)

    self.ui.main_frame_layout.addLayout(self.start_job_layout)
    self.ui.main_frame_layout.addStretch()
    self.setMaximumSize(461, 600)
    self.init_ui()
    self.setWindowIcon(QtGui.QIcon(str(model_definitions.ModelDefinitions.LOGO_FILEPATH)))
    self.setWindowTitle("LigParGen GUI")

  # <editor-fold desc="Util">
  def a_result_is_toggled(self) -> bool:
    """Checks if at least one of the resulting files are checked."""
    if self.action_apbs_pqr.isChecked():
      return True
    if self.action_charmm_pdb.isChecked():
      return True
    if self.action_charmm_prm.isChecked():
      return True
    if self.action_charmm_rtf.isChecked():
      return True
    if self.action_desmond_cms.isChecked():
      return True
    if self.action_gromacs_gro.isChecked():
      return True
    if self.action_gromacs_itp.isChecked():
      return True
    if self.action_lammps_lmp.isChecked():
      return True
    if self.action_openmm_pdb.isChecked():
      return True
    if self.action_openmm_xml.isChecked():
      return True
    if self.action_q_lib.isChecked():
      return True
    if self.action_q_pdb.isChecked():
      return True
    if self.action_q_prm.isChecked():
      return True
    if self.action_tinker_xyz.isChecked():
      return True
    if self.action_tinker_key.isChecked():
      return True
    if self.action_xplor_param.isChecked():
      return True
    if self.action_xplor_top.isChecked():
      return True
    return False

  def toggle_all_results(self) -> None:
    """Checks all actions of all result types."""
    actions = [
      self.action_apbs_pqr, self.action_charmm_pdb, self.action_charmm_prm,
      self.action_charmm_rtf, self.action_desmond_cms, self.action_gromacs_gro,
      self.action_gromacs_itp, self.action_lammps_lmp, self.action_openmm_pdb,
      self.action_openmm_xml, self.action_q_lib, self.action_q_pdb,
      self.action_q_prm, self.action_tinker_xyz, self.action_tinker_key,
      self.action_xplor_param, self.action_xplor_top
    ]
    for action in actions:
      action.setChecked(True)

  def untoggle_all_results(self) -> None:
    """Unchecks all actions of all result types."""
    actions = [
      self.action_apbs_pqr, self.action_charmm_pdb, self.action_charmm_prm,
      self.action_charmm_rtf, self.action_desmond_cms, self.action_gromacs_gro,
      self.action_gromacs_itp, self.action_lammps_lmp, self.action_openmm_pdb,
      self.action_openmm_xml, self.action_q_lib, self.action_q_pdb,
      self.action_q_prm, self.action_tinker_xyz, self.action_tinker_key,
      self.action_xplor_param, self.action_xplor_top
    ]
    for action in actions:
      action.setChecked(False)

  def get_toggled_result_types(self) -> list:
    """Gets all result types that are toggled.

    Returns:
      A list of checked result types.
    """
    tmp_result_types: list = []
    if self.action_apbs_pqr.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.APBS_PQR)
    if self.action_charmm_pdb.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.CHARMM_PDB)
    if self.action_charmm_prm.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.CHARMM_PRM)
    if self.action_charmm_rtf.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.CHARMM_RTF)
    if self.action_desmond_cms.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.DESMOND_CMS)
    if self.action_gromacs_gro.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.GROMACS_GRO)
    if self.action_gromacs_itp.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.GROMACS_ITP)
    if self.action_lammps_lmp.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.LAMMPS_LMP)
    if self.action_openmm_pdb.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.OPENMM_PDB)
    if self.action_openmm_xml.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.OPENMM_XML)
    if self.action_q_lib.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.Q_LIB)
    if self.action_q_pdb.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.Q_PDB)
    if self.action_q_prm.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.Q_PRM)
    if self.action_tinker_xyz.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.TINKER_XYZ)
    if self.action_tinker_key.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.TINKER_KEY)
    if self.action_xplor_param.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.XPLOR_PARAM)
    if self.action_xplor_top.isChecked():
      tmp_result_types.append(model_definitions.LigParGenResultFileTypes.XPLOR_TOP)
    return tmp_result_types
  # </editor-fold>

  # <editor-fold desc="Basic">
  def closeEvent(self, event) -> None:  # noqa: ANN001
    """Overrides the closeEvent of the QMainWindow class.

    Args:
      event: The event object representing the close event.
    """
    # <editor-fold desc="Checks">
    safeguard.CHECK(event is not None)
    # </editor-fold>
    # Emit the custom signal when the window is closed
    self.dialogClosed.emit(("", event))

  def init_ui(self) -> None:
    """Initialize the UI elements."""
    self.cbox_mol_optimization_iter.addItems(model_definitions.LigParGenOptions.MOLECULE_OPTIMIZATION_ITERATIONS)
    self.cbox_charge_model.addItems(model_definitions.LigParGenOptions.CHARGE_MODEL)
    self.cbox_molecule_charge.addItems(model_definitions.LigParGenOptions.MOLECULE_CHARGE)
    self.cbox_mol_optimization_iter.setFixedWidth(95)
    self.cbox_charge_model.setFixedWidth(95)
    self.cbox_molecule_charge.setFixedWidth(95)

  def block_gui(self) -> None:
    """Blocks the complete gui."""
    self.btn_structure_input.setEnabled(False)
    self.txt_structure_input.setEnabled(False)
    if self.accordion_section_options.content.isVisible():
      self.accordion_section_options.toggle_content()
    self.accordion_section_options.setEnabled(False)
    if self.accordion_section_results.content.isVisible():
      self.accordion_section_results.toggle_content()
    self.accordion_section_results.setEnabled(False)
    self.btn_start_job.setEnabled(False)

  def add_error_message_labels(self) -> None:
    """Adds the error message label to the main frame."""
    # Calculate tooltip position just above the QLineEdit
    tooltip_x = self.txt_structure_input.geometry().x() + 120
    tooltip_y = self.txt_structure_input.geometry().y()
    # Convert back to main window's coordinate system
    self.lbl_error_message = custom_label.ErrorMessageLabel(QtCore.QPoint(tooltip_x, tooltip_y), self)

  # </editor-fold>
