import React from "react";
import {Button} from "reactstrap";
import "./collections.css"

const Record = (props) => {
  return (
    <Button
        href={props.url}
        className="listItem"
        >
        {props.obj.map((field) => {
            if (props.obj[field] === null) {
                return <div key={field}>{field}: N/A</div>;
            } else if (
                props.obj[field].constructor === {}.constructor
            ) {

            let child_keys = Object.keys(props.obj[field]);

            if (field === "user")
            {
                return (
                <div key={field}>
                    Username:{" "}{props.obj[field].username}
                    <br />
                    Name:{" "}{props.obj[field]["first_name"]}{" "}
                    {props.obj[field]["last_name"]}
                </div>
                );
            } else if (field === "project") {
                return (
                <div key={field}>
                    Project Name:{" "}{props.obj[field]["name"]}
                </div>
                );
            } else {
                return (
                <div>
                    {field}:{" "}
                    {child_keys.map((child_field) => {
                    return (
                        <div key={child_field}>
                        {child_field}:{" "}
                        {props.obj[field][child_field]}
                        </div>
                    );
                    })}
                </div>
                );
            }
            } else {
            return (
                <div key={field}>
                {field}:{" "}{props.obj[field][field]}
                </div>
            );
            }
        })}
        </Button>
  );
};

export default Record;
