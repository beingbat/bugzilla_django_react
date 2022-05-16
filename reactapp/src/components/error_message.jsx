import React from "react";

const ErrorMessage = (props) => {
  return (
    <div className="badge bg-danger">
      <strong>Error Message:</strong>: {props.msg}
    </div>
  );
};

export default ErrorMessage;
