import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./collections.css";
import { Container, Row, Button } from "reactstrap";
import NotFound from "./notfound";
import ErrorMessage from "./error_message";
import Record from "./object";

const Collection = () => {
  const [collection, setCollection] = useState("");
  let api_url = "";
  let object_url = "";
  let url_correct = false;
  let { id } = useParams();
  id = id.toString();
  if (id === "project-collection") {
    api_url = "projects";
    object_url = "projects/";
    url_correct = true;
  } else if (id === "bug-collection") {
    api_url = "bugs";
    object_url = "bugs/";
    url_correct = true;
  } else if (id === "developer-collection") {
    api_url = "users/developer";
    object_url = "users/";
    url_correct = true;
  } else if (id === "qae-collection") {
    api_url = "users/qaengineer";
    object_url = "users/";
    url_correct = true;
  }

  const url = "http://127.0.0.1:8000/api/" + api_url;

  useEffect(() => {
    console.log(url);
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setCollection(json);
      } catch (error) {
        console.log("error", error);
      }
    };

    fetchData();
  });

  if (url_correct === false) {
    return <NotFound />;
  }

  const getCollection = () => {
    if (collection === "") {
      return <div>Nothing Found!</div>;
    } else {
      const collection_keys = Object.keys(collection);
      return (
        <Container>
          <Row>
            {collection_keys.map((key) => {
              if (key === "error_message") {
                return <ErrorMessage msg={collection_keys[key]} />;
              } else {
                let url = "/"
                if (id === "project-collection") {
                  url += object_url + collection_keys[key]["id"];
                } else if (id === "bug-collection") {
                  url += object_url + collection_keys[key]["uuid"];
                } else if (
                  id === "qae-collection" ||
                  id === "developer-collection"
                ) {
                  url += object_url + collection_keys[key]["user"]["id"];
                } else {
                  url = "#";
                }

                return <Record obj={collection_keys[key]} href={url} />;
              }
            })}
          </Row>
        </Container>
      );
    }
  };
  return <div>{getCollection()}</div>;
};

export default Collection;
