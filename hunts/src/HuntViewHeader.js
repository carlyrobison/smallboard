import React from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  selectNumUnlocked,
  selectNumSolved,
  selectNumUnsolved,
  selectNumMetasSolved,
} from "./puzzlesSlice";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ReactTooltip from "react-tooltip";

function HuntViewHeader({ hunt }) {
  const dispatch = useDispatch();

  const numUnlocked = useSelector(selectNumUnlocked);
  const numSolved = useSelector(selectNumSolved);
  const numUnsolved = useSelector(selectNumUnsolved);
  const numMetasSolved = useSelector(selectNumMetasSolved);
  const driveRedirect = hunt.has_drive ? (
    <div className="row">
      <ReactTooltip place="bottom" />
      <a data-tip="Create your drawings, jamboards, etc here" href={"drive"}>
        Google Drive Folder
      </a>
    </div>
  ) : null;

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          padding: "2px",
          alignItems: "center",
        }}
        className="row justify-content-between"
      >
        <h1 className="col-10">{hunt.name} - All Puzzles</h1>

        <div className="col-2">
          <a className="row " href={"stats"}>
            Hunt Statistics
          </a>
          {driveRedirect}
        </div>
      </div>
      <Container fluid>
        <Row className="text-center font-weight-bold small">
          <Col xs={1} className="text-nowrap">
            Metas Solved
          </Col>
          <Col xs={1}>Solved</Col>
          <Col xs={1}>Unsolved</Col>
          <Col xs={1}>Unlocked</Col>
        </Row>
        <Row className="text-center font-weight-bold">
          <Col xs={1} className="text-primary">
            {numMetasSolved}
          </Col>
          <Col xs={1} className="text-success">
            {numSolved}
          </Col>
          <Col xs={1} className="text-danger">
            {numUnsolved}
          </Col>
          <Col xs={1} className="text-secondary">
            {numUnlocked}
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default HuntViewHeader;
