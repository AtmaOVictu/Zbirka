"""
Main Window — TAZV Comprehension Machine z PREVERBA cevovodom
================================================================

"ZAJEMI O → REŽI ⊘ → POKAŽI ∆ → PREVERI ⊢ → SHRANI ∮"

Vsak gumb je ena faza R-7:
  ZAJEMI O: ∅ (praznina) — Zajemi celotno polje
  REŽI ⊘: ¬ (ločitev) — Naredi rez
  POKAŽI ∆: ∆ (razlika) — Pokaži razliko
  PREVERI ⊢: 1 / ⧖ (dejanje/izgovor) — Sam test (5 preizkusov + soma)
  SHRANI ∮: ∮ / ⟡ (povratek/nova možnost) — Shrani dokaz

Korpus:
  "Preverba je tresenje."
  "Telo je polje preverbe (⊥ = polje preverbe)."
  "Preverba soma je vedno človeška."
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QTabWidget,
                              QMessageBox, QTextEdit, QFrame)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont

from comprehension.core.processing_pipeline import ProcessingPipeline
from comprehension.core.symbol_mapper import SymbolMapper
from comprehension.core.preverba import Preverba
from comprehension.core.soma import SomaCheck, SomaPrompt
from comprehension.core.trainarium import Trainarium, TrainariumDrill
from comprehension.core.cadence import Kadenca, R7Phase, KadencaPreverba

from .r7_progress import R7ProgressWidget
from .module_window import ModuleWindow
from .knowledge_renderer import KnowledgeRenderer


# ── DELAVNI PROSTOR (WorkSpace) ──

class WorkSpace:
    """
    Delavni prostor za PREVERBA cevovod.
    
    Hrani:
      - trenutni vhod (statement)
      - trenutno fazo
      - rezultat preverbe
      - somatske podatke
      - drille (TRAINARIUM)
    """
    
    def __init__(self):
        self.preverba = Preverba()
        self.soma = SomaCheck()
        self.trainarium = Trainarium()
        self.kadenca = Kadenca()
        
        # Trenutno stanje
        self.current_statement = ""
        self.current_module = "MACRO"
        self.current_phase = R7Phase.PRAZNINA
        self.current_test_id = None
        
        # Režim
        self.workflow_mode = "CEVOVOD"  # CEVOVOD, AUTO, MANUAL
        
        # Zvezni objekt za integracijo
        self.kadenca_preverba = KadencaPreverba(
            preverba=self.preverba,
            soma_check=self.soma,
            trainarium=self.trainarium
        )
        
        # Registriraj callbacke
        self.kadenca_preverba.register_preverba_callbacks(self.kadenca)
    
    def set_statement(self, statement: str):
        """Nastavi novo trditev."""
        self.current_statement = statement
        self.current_test_id = None
    
    def zajemi(self, statement: str):
        """
        Faza ∅: Zajemi celotno polje.
        
        Korpus: "Zajemi surov vhod — trditev, besedo, stanje, preslikavo. Brez filtriranja."
        """
        self.set_statement(statement)
        self.current_phase = R7Phase.PRAZNINA
        self.current_module = "MACRO"
        
        # Kadenca: korak v nov cikel
        self.kadenca.mikro.state.reset_cycle()
        
        return {
            "phase": "∅",
            "action": "zajem polja",
            "statement": statement,
            "module": "MACRO",
            "result": "PASS",
        }
    
    def rezi(self, statement: str):
        """
        Faza ¬: Naredi rez.
        
        Korpus: "Razčleni. Loči signal od šuma. Uveljavi operator."
        """
        if not self.current_statement:
            return {"phase": "¬", "error": "Ni zajetega polja"}
        
        self.current_phase = R7Phase.LOCITVE
        self.current_module = "MMARK"
        
        # Simuliraj razčlenitev
        # TODO: Integracija z MMARK modulum
        
        # Kadenca: korak
        self.kadenca.on_operation("MMARK", statement)
        
        return {
            "phase": "¬",
            "action": "rez/razčlenitev",
            "statement": statement,
            "module": "MMARK",
            "result": "PASS",
        }
    
    def pokazi(self, statement: str):
        """
        Faza ∆: Pokaži razliko.
        
        Korpus: "Kaj se je spremenilo? Kaj je novo stanje? Kaj je prehod?"
        """
        if not self.current_statement:
            return {"phase": "∆", "error": "Ni rezanega polja"}
        
        self.current_phase = R7Phase.RAZLIKA
        self.current_module = "STATE"
        
        # Kadenca: korak
        self.kadenca.on_operation("STATE", statement)
        
        return {
            "phase": "∆",
            "action": "pokaži razliko",
            "statement": statement,
            "module": "STATE",
            "result": "PASS",
        }
    
    def preveri(self, statement: str = None):
        """
        Faza ⧖: Sam test.
        
        Korpus:
          "Ali prehod drži? Ali telo potrjuje? Ali preslikava preživi 5 preizkusov?"
          "Preverba soma je vedno človeška."
        
        VRNE: (rezultat, ego_flag, soma_flag)
        """
        if statement:
            self.set_statement(statement)
        
        if not self.current_statement:
            return {"phase": "⧖", "error": "Ni trditve za preverbo"}
        
        self.current_phase = R7Phase.TEST
        self.current_module = "VISUALIZATION"
        
        # 1. Odpelji 5 preizkusov
        modul = self.current_module
        trditev = self.current_statement
        
        rezultat, ego_flag, _ = self.preverba.run_5_tests(modul, trditev)
        
        # 2. Odpelji SOMA_PROMPT
        if rezultat == "PASS":
            soma_ok, flag = self.soma.check(modul, trditev)
            if not soma_ok:
                rezultat = "FAIL"
                soma_flag = True
                reason = flag
            elif flag:
                reason = flag
        else:
            soma_ok = False
            soma_flag = True
            reason = "Preizkusi padli"
        
        # 3. Če je FAIL, ustvari drill
        if rezultat == "FAIL":
            fail_type = "ego" if ego_flag else "unknown"
            fail_reason = reason or "Neznan razlog"
            
            drill = self.trainarium.create_drill(
                test_id=f"AUTO_{self.kadenca.mikro.state.cycle_count}",
                modul=modul,
                trditev=trditev,
                fail_type=fail_type,
                fail_reason=fail_reason,
            )
            
            # Izvede drill
            self.trainarium.run_drill(drill.drill_id)
        
        # 4. Logiraj v proof_log
        import datetime
        self.current_test_id = f"TEST_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        soma_desc = self.soma.get_soma_description()
        
        kanon_status = self.preverba.get_kanon_status(modul, trditev)
        
        self.preverba.log_proof(
            test_id=self.current_test_id,
            modul=modul,
            trditev=trditev,
            faza="⧖",
            rezultat=rezultat,
            soma=soma_desc,
            dokaz=f"preverba v fazi ⧖",
            doctrinarium=f"egoflag: {ego_flag}, somafag: {soma_flag}" if rezultat == "FAIL" else None,
            kanon_status=kanon_status,
        )
        
        # Kadenca: korak (spremeni v naslednjo fazo)
        self.kadenca.on_operation(modul, trditev)
        
        return {
            "phase": "⧖",
            "action": "preveri",
            "statement": trditev,
            "module": modul,
            "result": rezultat,
            "ego_flag": ego_flag,
            "soma_flag": soma_flag if rezultat == "FAIL" else False,
            "soma_desc": soma_desc,
            "test_id": self.current_test_id,
            "drill_created": rezultat == "FAIL",
        }
    
    def shrani(self, statement: str = None):
        """
        Faza ∮: Shrani dokaz.
        
        Korpus:
          "Shrani dokaz. Arhiviraj."
          "Če drži → vstopi v kanon. Če poči → vstopi v TRAINARIUM kot drill."
        """
        if statement:
            self.set_statement(statement)
        
        if not self.current_statement:
            return {"phase": "∮", "error": "Ni trditve za shranjevanje"}
        
        self.current_phase = R7Phase.POVRATEK
        self.current_module = "VISUALIZATION"
        
        modul = self.current_module
        trditev = self.current_statement
        
        # Preveri, ali je to PASS ali FAIL
        # V resnici: preveri zadnji test
        last_test = self.preverba.get_last_test(modul, trditev, "čas")
        
        if last_test and last_test[4] == "PASS":  # rezultat je na indexu 4
            # Vstopi v kanon
            new_status = "KANON" if last_test[9] == "PREVERJEN" else "PREVERJEN"
            self.preverba.update_kanon_status(modul, trditev, new_status)
            
            kanon_action = "vstop v kanon"
        else:
            # Vstopi v TRAINARIUM
            kanon_action = "vstop v TRAINARIUM"
        
        # Kadenca: korak
        self.kadenca.on_operation(modul, trditev)
        
        return {
            "phase": "∮",
            "action": "shrani",
            "statement": trditev,
            "module": modul,
            "result": "PASS",
            "kanon_action": kanon_action,
        }
    
    def get_active_drills(self):
        """VRNE: aktivne drille za prikaz v UI."""
        return self.trainarium.get_active_drills()
    
    def get_soma_actions(self):
        """VRNE: mikro-akcije za uporabnika (iz SOMA_CHECK)."""
        return self.trainarium.get_dejanje_for_user("SYSTEM")


# ── PIPELINE WORKER (za asinhrono obdelavo) ──

class PipelineWorker(QThread):
    phase_completed = pyqtSignal(str, str, dict)
    pipeline_done = pyqtSignal(object)
    pipeline_error = pyqtSignal(str)

    def __init__(self, pipeline, statement):
        super().__init__()
        self.pipeline = pipeline
        self.statement = statement

    def run(self):
        try:
            result = self.pipeline.process(self.statement)
            for phase, output in result.phases.items():
                self.phase_completed.emit(phase, output.module_name, {
                    "data": output.data,
                    "kpi": output.kpi,
                    "status": output.status,
                    "duration_ms": output.duration_ms,
                })
            self.pipeline_done.emit(result)
        except Exception as e:
            self.pipeline_error.emit(str(e))


# ── MAIN WINDOW ──

class MainWindow(QMainWindow):
    """
    Glavno okno TAZV Comprehension Machine z PREVERBA cevovodom.
    
    Ima:
      - Input polje za trditve
      - 5 gumbe: ZAJEMI O, REŽI ⊘, POKAŽI ∆, PREVERI ⊢, SHRANI ∮
      - Tabi za module
      - Status bar z R7 progresom
      - SOMA_PROMPT integracijo
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — PREVERBA")
        self.resize(1000, 700)
        
        # Inicializiraj pipeline in mapper
        self.pipeline = ProcessingPipeline()
        self.mapper = SymbolMapper()
        self.worker = None
        
        # Inicializiraj WorkSpace
        self.workspace = WorkSpace()
        
        # Stili
        ss = (
            "QMainWindow{background:#1a1a1a;color:#c0c0c0;}"
            "QWidget{background:#1a1a1a;color:#c0c0c0;}"
            "QLineEdit{background:#2a2a2a;color:#c0ffc0;border:1px solid #404040;padding:4px;}"
            "QPushButton{background:#2a4a2a;color:#c0ffc0;border:1px solid #40a040;padding:6px 16px;}"
            "QPushButton:hover{background:#3a5a3a;}"
            "QPushButton:disabled{background:#2a2a2a;color:#606060;}"
            "QTextEdit{background:#0a0a0a;color:#c0ffc0;border:1px solid #303030;}"
            "QTabWidget::pane{border:1px solid #303030;}"
            "QTabBar::tab{background:#1a1a1a;color:#808080;padding:8px 16px;border:1px solid #303030;}"
            "QTabBar::tab:selected{background:#2a4a2a;color:#c0ffc0;}"
            "QStatusBar{background:#0a0a0a;color:#808080;}"
            "QMenuBar{background:#1a1a1a;color:#c0c0c0;}"
            "QMenuBar::item:selected{background:#2a4a2a;}"
            "QLabel{color:#c0c0c0;}"
            "QFrame{background:#0a0a0a;border:1px solid #303030;padding:8px;}"
        )
        self.setStyleSheet(ss)
        
        # Central widget
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # ─── PREVERBA CEVOVOD (5 gumbov) ───
        
        # Input row
        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Statement:"))
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.process_statement)
        self.input.setPlaceholderText("Vnesi trditev, besedo, stanje ali preslikavo...")
        input_row.addWidget(self.input, stretch=1)
        layout.addLayout(input_row)
        
        # Cevovod buttons
        cevovod_row = QHBoxLayout()
        cevovod_row.setSpacing(4)
        
        # ZAJEMI O (∅)
        self.btn_zajemi = QPushButton("ZAJEMI O (∅)")
        self.btn_zajemi.clicked.connect(self.zajemi)
        self.btn_zajemi.setToolTip("Faza ∅: Zajemi celotno polje. Vzemi surov vhod — trditev, besedo, stanje, preslikavo. Brez filtriranja.")
        cevovod_row.addWidget(self.btn_zajemi)
        
        # REŽI ⊘ (¬)
        self.btn_rezi = QPushButton("REŽI ⊘ (¬)")
        self.btn_rezi.clicked.connect(self.rezi)
        self.btn_rezi.setToolTip("Faza ¬: Naredi rez. Razčleni. Loči signal od šuma. Uveljavi operator.")
        cevovod_row.addWidget(self.btn_rezi)
        
        # POKAŽI ∆ (∆)
        self.btn_pokazi = QPushButton("POKAŽI ∆ (∆)")
        self.btn_pokazi.clicked.connect(self.pokazi)
        self.btn_pokazi.setToolTip("Faza ∆: Pokaži razliko. Kaj se je spremenilo? Kaj je novo stanje? Kaj je prehod?")
        cevovod_row.addWidget(self.btn_pokazi)
        
        # PREVERI ⊢ (⧖)
        self.btn_preveri = QPushButton("PREVERI ⊢ (⧖)")
        self.btn_preveri.clicked.connect(self.preveri)
        self.btn_preveri.setToolTip("Faza ⧖: Sam test. Ali prehod drži? Ali telo potrjuje? Ali preslikava preživi 5 preizkusov?")
        cevovod_row.addWidget(self.btn_preveri)
        
        # SHRANI ∮ (∮)
        self.btn_shrani = QPushButton("SHRANI ∮ (∮)")
        self.btn_shrani.clicked.connect(self.shrani)
        self.btn_shrani.setToolTip("Faza ∮: Shrani dokaz. Arhiviraj. Če drži → vstopi v kanon. Če poči → vstopi v TRAINARIUM kot drill.")
        cevovod_row.addWidget(self.btn_shrani)
        
        layout.addLayout(cevovod_row)
        
        # Process button (original)
        process_row = QHBoxLayout()
        self.btn_process = QPushButton("Process (R-7 Pipeline)")
        self.btn_process.clicked.connect(self.process_statement)
        process_row.addWidget(self.btn_process)
        
        # Trajnost check
        self.btn_check_soma = QPushButton("SOMA CHECK")
        self.btn_check_soma.clicked.connect(self.check_soma)
        process_row.addWidget(self.btn_check_soma)
        
        # Drills gumb
        self.btn_show_drills = QPushButton("TRAINARIUM")
        self.btn_show_drills.clicked.connect(self.show_drills)
        process_row.addWidget(self.btn_show_drills)
        
        layout.addLayout(process_row)
        
        # Output text area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 10))
        self.output.setMaximumHeight(150)
        layout.addWidget(self.output)
        
        # ─── TABI (moduli) ───
        self.tabs = QTabWidget()
        self.modules = {}
        for item in self.mapper.get_r7_symbols():
            mw = ModuleWindow(item["system"], item["module"])
            self.modules[item["system"]] = mw
            label = item["system"] + " " + item["module"]
            self.tabs.addTab(mw, label)
        self.tabs.addTab(KnowledgeRenderer(), "Index")
        layout.addWidget(self.tabs, stretch=1)
        
        self.setCentralWidget(central)
        
        # ─── STATUS BAR ───
        self.progress = R7ProgressWidget()
        self.statusBar().addWidget(self.progress)
        self.statusBar().showMessage("Ready — PREVERBA cevovod")
        
        # Menu
        m = self.menuBar()
        fm = m.addMenu("File")
        fm.addAction("Clear", self.clear_all)
        fm.addAction("Exit", self.close)
        
        # Debug menu
        dm = m.addMenu("Debug")
        dm.addAction("Test Preverba", self.test_preverba)
        dm.addAction("Test SOMA", self.test_soma)
        dm.addAction("Test Trainarium", self.test_trainarium)
        dm.addAction("Test Cadence", self.test_cadence)
    
    # ─── PREVERBA METODE ───
    
    def zajemi(self):
        """Ob kliku ZAJEMI O."""
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Vnesi trditev.")
            return
        
        result = self.workspace.zajemi(text)
        self._display_preverba_result(result)
        self.statusBar().showMessage(f"∅ ZAJEMI: {result.get('statement', '')}")
    
    def rezi(self):
        """Ob kliku REŽI ⊘."""
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Vnesi trditev.")
            return
        
        result = self.workspace.rezi(text)
        self._display_preverba_result(result)
        self.statusBar().showMessage(f"¬ REŽI: {result.get('statement', '')}")
    
    def pokazi(self):
        """Ob kliku POKAŽI ∆."""
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Vnesi trditev.")
            return
        
        result = self.workspace.pokazi(text)
        self._display_preverba_result(result)
        self.statusBar().showMessage(f"∆ POKAŽI: {result.get('statement', '')}")
    
    def preveri(self):
        """Ob kliku PREVERI ⊢."""
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Vnesi trditev.")
            return
        
        result = self.workspace.preveri(text)
        self._display_preverba_result(result)
        
        # Prikaz SOMA_PROMPT poročila
        if result.get("soma_desc"):
            self.output.append(f"SOMA: {result['soma_desc']}")
        
        # Prikaz drilla, če je bil ustvarjen
        if result.get("drill_created"):
            self.output.append("⚠️ DRILL USTVARJEN (glej TRAINARIUM)")
            self.show_drills()
        
        status = "PASS" if result.get("result") == "PASS" else "FAIL"
        self.statusBar().showMessage(f"⧖ PREVERI: {status}")
        
        # Kadenca: sprotni korak
        self.workspace.kadenca.on_operation("VISUALIZATION", text)
    
    def shrani(self):
        """Ob kliku SHRANI ∮."""
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Vnesi trditev.")
            return
        
        result = self.workspace.shrani(text)
        self._display_preverba_result(result)
        self.statusBar().showMessage(f"∮ SHRANI: {result.get('kanon_action', '')}")
    
    def _display_preverba_result(self, result: dict):
        """Prikazi rezultat preverbe v output."""
        phase = result.get("phase", "?")
        action = result.get("action", "")
        statement = result.get("statement", "")
        modul = result.get("module", "")
        status = result.get("result", "")
        
        msg = f"[{phase}] {action}: {statement} ({modul}) → {status}"
        self.output.append(msg)
        
        # Če je error
        if result.get("error"):
            self.output.append(f"  ERROR: {result['error']}")
    
    def check_soma(self):
        """Preveri SOMA stanja."""
        text = self.input.text().strip()
        if not text:
            text = "test"
        
        soma_ok, flag = self.workspace.soma.check("SYSTEM", text)
        soma_desc = self.workspace.soma.get_soma_description()
        
        if soma_ok:
            self.output.append(f"✓ SOMA CHECK: PASS — {soma_desc}")
        else:
            self.output.append(f"✗ SOMA CHECK: FAIL — {flag} — {soma_desc}")
        
        self.statusBar().showMessage(f"SOMA: {'PASS' if soma_ok else 'FAIL'}")
    
    def show_drills(self):
        """Prikaži aktivne drille."""
        drills = self.workspace.trainarium.get_active_drills()
        
        if not drills:
            QMessageBox.information(self, "TRAINARIUM", "Ni aktivnih drillov.")
            return
        
        msg = "Aktivni DRILL-i:\n\n"
        for drill in drills:
            msg += f"• {drill.drill_id} ({drill.modul}): {drill.fail_type}\n"
            msg += f"  Beseda: {drill.beseda[:50]}...\n"
            msg += f"  Dejanje: {drill.dejanje[:50]}...\n\n"
        
        QMessageBox.information(self, "TRAINARIUM", msg)
    
    # ─── ORIGINAL PIPELINE METODE ───
    
    def process_statement(self):
        """Originalna obdelava trditve (R-7 pipeline)."""
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Enter a statement.")
            return
        
        self.btn_process.setEnabled(False)
        for phase in ["∅", "¬", "∆", "⧖", "∮", "⟡"]:
            self.btn_zajemi.setEnabled(phase == "∅")
            self.btn_rezi.setEnabled(phase == "¬")
            self.btn_pokazi.setEnabled(phase == "∆")
            self.btn_preveri.setEnabled(phase == "⧖")
            self.btn_shrani.setEnabled(phase == "∮")
        
        self.progress.reset()
        for mw in self.modules.values():
            mw.clear()
        self.statusBar().showMessage("Processing...")
        
        self.worker = PipelineWorker(self.pipeline, text)
        self.worker.phase_completed.connect(self.on_phase)
        self.worker.pipeline_done.connect(self.on_done)
        self.worker.pipeline_error.connect(self.on_error)
        self.worker.start()
    
    def on_phase(self, phase, module, data):
        """Ob koncu fase v pipeline-u."""
        idx = self.mapper.R7_ORDER.index(phase) if phase in self.mapper.R7_ORDER else -1
        self.progress.set_phase(idx)
        if phase in self.modules:
            self.modules[phase].display(data)
        status = data.get("status", "?")
        msg = f"{phase} ({module}): {status}"
        self.statusBar().showMessage(msg)
    
    def on_done(self, result):
        """Ob koncu pipeline-a."""
        self.btn_process.setEnabled(True)
        for phase in ["∅", "¬", "∆", "⧖", "∮", "⟡"]:
            self.btn_zajemi.setEnabled(True)
            self.btn_rezi.setEnabled(True)
            self.btn_pokazi.setEnabled(True)
            self.btn_preveri.setEnabled(True)
            self.btn_shrani.setEnabled(True)
        
        errors = len(result.all_errors)
        msg = f"Done: {result.status} | {result.total_duration_ms:.1f}ms | {errors} errors"
        self.statusBar().showMessage(msg)
        self.output.append(f"PIPELINE: {msg}")
    
    def on_error(self, msg):
        """Ob napaki v pipeline-u."""
        self.btn_process.setEnabled(True)
        for phase in ["∅", "¬", "∆", "⧖", "∮", "⟡"]:
            self.btn_zajemi.setEnabled(True)
            self.btn_rezi.setEnabled(True)
            self.btn_pokazi.setEnabled(True)
            self.btn_preveri.setEnabled(True)
            self.btn_shrani.setEnabled(True)
        
        self.statusBar().showMessage(f"Error: {msg}")
        self.output.append(f"ERROR: {msg}")
        QMessageBox.critical(self, "Error", msg)
    
    def clear_all(self):
        """Počisti vse."""
        self.input.clear()
        self.output.clear()
        for mw in self.modules.values():
            mw.clear()
        self.progress.reset()
        self.statusBar().showMessage("Ready")
    
    # ─── TEST METODE ───
    
    def test_preverba(self):
        """Test Preverba modula."""
        p = Preverba()
        rezultat, ego_flag, _ = p.run_5_tests("STATE", "RES011 → RES042")
        
        msg = f"Preverba test:\n"
        msg += f"  Rezultat: {rezultat}\n"
        msg += f"  Ego flag: {ego_flag}"
        
        QMessageBox.information(self, "Preverba Test", msg)
    
    def test_soma(self):
        """Test SOMA modula."""
        soma = SomaCheck()
        
        # Simuliraj tipkanje
        for i in range(10):
            soma.add_keypress()
            import time
            time.sleep(0.05)
        
        # Preveri
        soma_ok, flag = soma.check("TEST", "test trditev")
        desc = soma.get_soma_description()
        
        msg = f"SOMA Test:\n"
        msg += f"  Soma OK: {soma_ok}\n"
        msg += f"  Flag: {flag}\n"
        msg += f"  Opis: {desc}"
        
        QMessageBox.information(self, "SOMA Test", msg)
    
    def test_trainarium(self):
        """Test TRAINARIUM modula."""
        trainarium = Trainarium()
        
        drill = trainarium.create_drill(
            test_id="TEST_001",
            modul="APD",
            trditev="différance = ∂",
            fail_type="ego",
            fail_reason="kršitev §52",
        )
        
        msg = f"TRAINARIUM Test:\n"
        msg += f"  Drill ID: {drill.drill_id}\n"
        msg += f"  Beseda: {drill.beseda}\n"
        msg += f"  Stavek: {drill.stavek}\n"
        msg += f"  Dejanje: {drill.dejanje}"
        
        QMessageBox.information(self, "Trainarium Test", msg)
    
    def test_cadence(self):
        """Test CADENCE modula."""
        kadenca = Kadenca()
        
        msg = "CADENCE Test:\n\n"
        msg += "Simulacija 7 operacij:\n"
        
        for i in range(7):
            old, new = kadenca.on_operation("TEST", f"op_{i+1}")
            msg += f"  {old.value} → {new.value}\n"
        
        stats = kadenca.get_cycle_stats()
        msg += f"\nStatistika:\n"
        for k, v in stats.items():
            msg += f"  {k}: {v}\n"
        
        QMessageBox.information(self, "Cadence Test", msg)


# Fix for datetime import in workspace
import datetime


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
