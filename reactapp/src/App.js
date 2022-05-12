import './App.css'
import React, { useEffect, useState } from 'react'
import './App.css';

const App = () => {
  const [projectlist, setProjectList] = useState('');

  useEffect(() => {
    const url = 'http://127.0.0.1:8000/api/projects';

    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        console.log(json);
        setProjectList(json);
        console.log("project list: ", projectlist);
      } catch (error) {
        console.log('error', error);
      }
    }

    fetchData()
  });

  const getData =()=>
  {
    if (projectlist !== '')
    {
      const keys = Object.keys(projectlist)
      console.log(projectlist)
      console.log(keys)
      return (<>{keys.map((key)=>
      {
        if (key==="error_message")
        {
          return (<div className="badge bg-danger error_message"><div className="text_div">Error Message: {projectlist[key]}</div></div>)
        }
        else
        {
          return (<div className="listItem">
          <li>{projectlist[key].name}</li>
            <li>{projectlist[key].description}</li>
            </div>)
        }

          })}</>);

    }

  }


  return (
    <div>
      <p>
        {getData()}
      </p>
    </div>
  )
}

export default App;
