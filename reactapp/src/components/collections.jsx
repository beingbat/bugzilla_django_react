import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const Collection = () => {
  let { id } = useParams();
  id = id.toString();
  const [projectlist, setProjectList] = useState("");
  let type = "";
  if (id === "project-collection") {
    type = "projects";
  } else if (id === "bug-collection") {
    type = "bugs";
  } else if (id === "developer-collection") {
    type = "users/developer";
  } else if (id === "qae-collection") {
    type = "users/qaengineer";
  }

  const url = "http://127.0.0.1:8000/api/" + type;

  useEffect(() => {
    console.log(url);
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setProjectList(json);
      } catch (error) {
        console.log("error", error);
      }
    };

    fetchData();
  });

  const getData = () => {
    if (projectlist !== "") {
      const keys = Object.keys(projectlist);
      return (
        <>
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
                <div className="listItem">
                  {project_fields.map((field) => {
                    console.log("field: ", field, " ", projectlist[key][field]);
                    if (projectlist[key][field] === null) {
                      return <div key={field}>{field}: N/A</div>;
                    } else if (
                      projectlist[key][field].constructor === {}.constructor
                    ) {
                      let v = Object.keys(projectlist[key][field]);
                      return (
                        <div>
                          {field}:
                          {v.map((subfields) => {
                            return (
                              <div>
                                &emsp;{subfields}:{" "}
                                {projectlist[key][field][subfields]}
                              </div>
                            );
                          })}
                        </div>
                      );
                    } else {
                      return (
                        <div key={field}>
                          {field}:{projectlist[key][field]}
                        </div>
                      );
                    }
                  })}
                </div>
              );
            }
          })}
        </>
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
