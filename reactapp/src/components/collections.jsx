import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./collections.css";
import { Container, Row, Button } from "reactstrap";

const Collection = () => {
  let { id } = useParams();
  id = id.toString();
  const [projectlist, setProjectList] = useState("");
  let type = "";
  let primary_key = "";
  let link = "";
  let url_correct = false;
  if (id === "project-collection") {
    type = "projects";
    link = "projects/";
    url_correct = true;
    primary_key = "id";
  } else if (id === "bug-collection") {
    type = "bugs";
    link = "bugs/";
    primary_key = "uuid";
    url_correct = true;
  } else if (id === "developer-collection") {
    type = "users/developer";
    link = "users/";
    url_correct = true;
    primary_key = "user";
  } else if (id === "qae-collection") {
    type = "users/qaengineer";
    link = "users/";
    primary_key = "user";
    url_correct = true;
  }

  const url = "http://127.0.0.1:8000/api/" + type;

  useEffect(() => {
    console.log(url);
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        console.log(json);
        setProjectList(json);
      } catch (error) {
        console.log("error", error);
      }
    };

    fetchData();
  });

  if (url_correct === false) {
    return (
      <div className="badge bg-danger error_message">
        <div className="text_div">
          Error Message: Page requested not found 404
        </div>
      </div>
    );
  }

  const getData = () => {
    if (projectlist !== "") {
      const keys = Object.keys(projectlist);
      return (
        <Container>
          <Row>
            {keys.map((key) => {
              if (key === "error_message") {
                return (
                  <div className="badge bg-danger error_message">
                    <div className="text_div">
                      Error Message: {projectlist[key]}
                    </div>
                  </div>
                );
              } else {
                const project_fields = Object.keys(projectlist[key]);
                return (
                  <Button
                    href={
                      primary_key === "user"
                        ? "/" + link + projectlist[key][primary_key]["id"]
                        : "/" + link + projectlist[key][primary_key]
                    }
                    className="listItem"
                  >
                    {project_fields.map((field) => {
                      if (projectlist[key][field] === null) {
                        return <div key={field}>{field}: N/A</div>;
                      } else if (
                        projectlist[key][field].constructor === {}.constructor
                      ) {
                        let v = Object.keys(projectlist[key][field]);

                        if (field === "user") {
                          return (
                            <div>
                              Username: {projectlist[key][field].username}
                              <br />
                              Name: {projectlist[key][field]["first_name"]}{" "}
                              {projectlist[key][field]["last_name"]}
                            </div>
                          );
                        } else if (field === "project") {
                          return (
                            <div>
                              Project Name: {projectlist[key][field]["name"]}
                            </div>
                          );
                        } else {
                          return (
                            <div>
                              {field}:{" "}
                              {v.map((subfields) => {
                                return (
                                  <div>
                                    {subfields}:{" "}
                                    {projectlist[key][field][subfields]}
                                  </div>
                                );
                              })}
                            </div>
                          );
                        }
                      } else {
                        return (
                          <div key={field}>
                            {field}: {projectlist[key][field]}
                          </div>
                        );
                      }
                    })}
                  </Button>
                );
              }
            })}
          </Row>
        </Container>
      );
    }
  };

  return (
    <div>
      <div>{getData()}</div>
    </div>
  );
};

export default Collection;
