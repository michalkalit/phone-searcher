import { useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import axios from "axios";

interface Props {
  onLoginSuccess: (phone: string) => void;
}

export default function LoginForm({ onLoginSuccess }: Props) {
  const [phoneInput, setPhoneInput] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const encoded = encodeURIComponent(phoneInput);
      const url = `${process.env.NEXT_PUBLIC_API_URL}/devices/${encoded}/gps`;

      const resp = await axios.post(url, {});

      if (resp.status >= 200 && resp.status < 300) {
        onLoginSuccess(phoneInput);
      } else {
        setError("Login failed. Please check your number.");
      }
    } catch {
      setError("Login failed. Please check your number.");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",

        justifyContent: "center",
        alignItems: "center",
        gap: 6,
        padding: 4,

      }}
    >
      <img
        src="/x-marks.png"
        alt="X marks icon"
        style={{ width: 260, height: "auto" }}
      />

      <Typography variant="h4" fontWeight={600} textAlign="center">
        X Marks The Phone
      </Typography>

      <form
        onSubmit={handleLogin}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 20,
          width: 300,
        }}
      >
        <TextField
          id="phone"
          label="Mobile Number"
          variant="outlined"
          value={phoneInput}
          onChange={(e) => setPhoneInput(e.target.value)}
          placeholder="+15551234567"
          InputProps={{ style: { fontSize: 18, padding: "14px" } }}
          InputLabelProps={{ style: { fontSize: 18 } }}
          required
        />

        <Button
          type="submit"
          variant="contained"
        >
          Sign In
        </Button>

        {error && (
          <Typography color="error" fontSize={16} textAlign="center">
            {error}
          </Typography>
        )}
      </form>
    </Box>
  );
}
