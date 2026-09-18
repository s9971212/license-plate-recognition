from sqlalchemy import select

from .models import Branch, Gate


class BranchRepository:

    def __init__(self, session):
        self.session = session

    # =========================================================
    # CREATE
    # =========================================================

    def create(
            self,
            branch_id: str,
            branch_name: str,
    ) -> Branch:

        branch = Branch(
            branch_id=branch_id,
            branch_name=branch_name,
        )

        self.session.add(branch)
        self.session.commit()
        self.session.refresh(branch)

        return branch

    # =========================================================
    # READ
    # =========================================================

    def get_by_id(
            self,
            branch_id: str,
    ) -> Branch | None:

        return self.session.get(
            Branch,
            branch_id,
        )

    def get_by_branch_name(
            self,
            branch_name: str,
    ) -> Branch | None:

        stmt = select(Branch).where(
            Branch.branch_name == branch_name
        )

        return self.session.scalar(stmt)

    def get_all(self) -> list[Branch]:

        stmt = select(Branch)

        return list(
            self.session.scalars(stmt).all()
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update_branch_name(
            self,
            branch_id: str,
            branch_name: str,
    ) -> Branch | None:

        branch = self.session.get(
            Branch,
            branch_id,
        )

        if branch is None:
            return None

        branch.branch_name = branch_name

        self.session.commit()
        self.session.refresh(branch)

        return branch

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
            self,
            branch_id: str,
    ) -> bool:

        branch = self.session.get(
            Branch,
            branch_id,
        )

        if branch is None:
            return False

        self.session.delete(branch)
        self.session.commit()

        return True


class GateRepository:

    def __init__(self, session):
        self.session = session

    # =========================================================
    # CREATE
    # =========================================================

    def create(
            self,
            gate_id: str,
            gate_name: str,
            ip: str,
    ) -> Gate:

        gate = Gate(
            gate_id=gate_id,
            gate_name=gate_name,
            ip=ip,
        )

        self.session.add(gate)
        self.session.commit()
        self.session.refresh(gate)

        return gate

    # =========================================================
    # READ
    # =========================================================

    def get_by_id(
            self,
            gate_id: str,
    ) -> Gate | None:

        return self.session.get(
            Gate,
            gate_id,
        )

    def get_by_gate_name(
            self,
            gate_name: str,
    ) -> Gate | None:

        stmt = select(Gate).where(
            Gate.gate_name == gate_name
        )

        return self.session.scalar(stmt)

    def get_by_branch_id(
            self,
            branch_id: str,
    ) -> list[Gate]:

        stmt = select(Gate).where(
            Gate.branch_id == branch_id
        )

        return list(
            self.session.scalars(stmt).all()
        )

    def get_by_branch_id_and_gate_ids(
            self,
            branch_id: str,
            gate_ids: list[str],
    ) -> list[Gate]:

        stmt = select(Gate).where(
            Gate.branch_id == branch_id,
            Gate.gate_id.in_(gate_ids),
        )

        return list(
            self.session.scalars(stmt).all()
        )

    def get_all(self) -> list[Gate]:

        stmt = select(Gate)

        return list(
            self.session.scalars(stmt).all()
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update_gate_name(
            self,
            gate_id: str,
            gate_name: str,
    ) -> Gate | None:

        gate = self.session.get(
            Gate,
            gate_id,
        )

        if gate is None:
            return None

        gate.gate_name = gate_name

        self.session.commit()
        self.session.refresh(gate)

        return gate

    def update_ip(
            self,
            gate_id: str,
            ip: str,
    ) -> Gate | None:

        gate = self.session.get(
            Gate,
            gate_id,
        )

        if gate is None:
            return None

        gate.ip = ip

        self.session.commit()
        self.session.refresh(gate)

        return gate

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
            self,
            gate_id: str,
    ) -> bool:

        gate = self.session.get(
            Gate,
            gate_id,
        )

        if gate is None:
            return False

        self.session.delete(gate)
        self.session.commit()

        return True
