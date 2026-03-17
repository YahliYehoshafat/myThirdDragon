import Form from 'react-bootstrap/Form';

function TextBox() {
  //A text box that allows the user to type the name of the new pet they want to create.
  return (
    <>
      <br />
      <Form.Control type="text" placeholder="Choose a name for your pet" size="lg" />
      <br />
    </>
  );
}

export default TextBox;