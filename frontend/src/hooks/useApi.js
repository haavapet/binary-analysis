const useApi = () => {
  const callApi = async (formData) => {
    var postFormData = new FormData();

    for (const name in formData) {
      // Arrays/lists needs to be encoded with key,value for each item in the array
      if (formData[name] instanceof Array) {
        postFormData.append(name, formData[name][0]);
        postFormData.append(name, formData[name][1]);
      } else {
        postFormData.append(name, formData[name]);
      }
    }

    return fetch(`http://${process.env.REACT_APP_BACKEND_URL || "localhost:8000"}/api`, {
      method: "POST",
      body: postFormData,
    }).then((response) => response.json());
  };

  return { callApi };
};

export default useApi;
