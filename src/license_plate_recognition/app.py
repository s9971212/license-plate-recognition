import logging
import threading
from types import SimpleNamespace

from .config import Config
from .database.database import Database
from .database.repository import BranchRepository, GateRepository
from .gate.gate_runner import GateRunner
from .logging_config import setup_logging

logger = logging.getLogger(__name__)


class Application:

    def __init__(self):

        # =========================
        # Logging
        # =========================

        setup_logging(Config.LOG_PATH)

        # =========================
        # Components
        # =========================

        self.db = Database()

        # 建立 Table
        # self.db.create_tables()

        # =========================
        # Threads
        # =========================

        self.threads = []

    def run(self):
        """
        啟動 Application
        """

        logger.info("Application 啟動")

        try:
            branch = self.get_branch()

            if branch is None:
                logger.error("找不到 Branch，Application 結束")
                return

            logger.info(
                "Branch: %s - %s",
                branch.branch_id,
                branch.branch_name,
            )

            gates = self.get_gates()

            if not gates:
                logger.warning("找不到任何 Gate，Application 結束")
                return

            logger.info(
                "取得 %d 個 Gate",
                len(gates),
            )

            self.start_gates(gates)

            self.wait_for_gates()

        except Exception:
            logger.exception("Application 發生未預期錯誤")

        finally:
            self.shutdown()

    def shutdown(self):
        """
        Application 結束時清理資源
        """

        try:
            self.db.dispose()

        except Exception:
            logger.exception("關閉 Database 時發生錯誤")

        logger.info("Application 已停止")

    # =========================================================
    # Branch
    # =========================================================

    def get_branch(self):
        """
        取得 Branch
        """

        # =========================
        # DEBUG
        # =========================

        if Config.DEBUG:
            logger.info("DEBUG 模式: 使用測試 Branch")

            return SimpleNamespace(
                branch_id="00",
                branch_name="測試",
            )

        # =========================
        # Production
        # =========================

        if not Config.BRANCH_ID:
            raise ValueError("BRANCH_ID 未設定")

        with self.db.get_session() as session:
            repo = BranchRepository(session)

            return repo.get_by_id(Config.BRANCH_ID)

    # =========================================================
    # Gate
    # =========================================================

    def get_gates(self):
        """
        取得 Branch 底下的 Gate
        """

        # =========================
        # DEBUG
        # =========================

        if Config.DEBUG:
            logger.info("DEBUG 模式: 使用測試 Gate")

            return [
                SimpleNamespace(
                    gate_id="1",
                    gate_name="測試1",
                    ip="192.168.1.123:123",
                )
            ]

        # =========================
        # Production
        # =========================

        if not Config.GATES:
            raise ValueError("GATES 未設定")

        with self.db.get_session() as session:
            repo = GateRepository(session)

            return repo.get_by_branch_id_and_gate_ids(
                branch_id=Config.BRANCH_ID,
                gate_ids=Config.GATES,
            )

    # =========================================================
    # Thread
    # =========================================================

    def start_gates(self, gates):
        """
        啟動所有 Gate Thread
        """

        for gate in gates:
            runner = GateRunner(gate)

            thread = threading.Thread(
                target=self.run_gate,
                args=(runner,),
                name=f"Gate-{gate.gate_id}",
                daemon=True,
            )

            thread.start()

            self.threads.append(thread)

            logger.info(
                "啟動 Gate: %s - %s",
                gate.gate_id,
                gate.gate_name,
            )

    # =========================================================
    # Gate Runner
    # =========================================================

    @staticmethod
    def run_gate(runner):
        """
        Gate Thread 執行入口
        """

        logger = logging.getLogger(threading.current_thread().name)

        try:
            runner.run()

        except Exception:
            logger.exception("Gate 執行發生錯誤")

    # =========================================================
    # Wait
    # =========================================================

    def wait_for_gates(self):
        """
        等待所有 Gate Thread
        """

        for thread in self.threads:
            logger.info(
                "等待 %s",
                thread.name,
            )

            thread.join()
