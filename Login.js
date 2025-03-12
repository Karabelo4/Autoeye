"use client"

import { useState } from "react"
import { View, TextInput, Button, StyleSheet, Text } from "react-native"
import api from "../services/api"

const Login = ({ navigation }) => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const handleLogin = async () => {
    try {
      const response = await api.post("/auth/login/", { username, password })
      if (response.status === 200) {
        setMessage("Login successful")
        // Navigate to Dashboard or Home screen
        navigation.navigate("Dashboard")
      }
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.message || "Login failed")
      } else {
        setMessage("An error occurred. Please try again.")
      }
    }
  }

  return (
    <View style={styles.container}>
      <TextInput style={styles.input} placeholder="Username" value={username} onChangeText={setUsername} />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Login" onPress={handleLogin} />
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 20,
  },
  input: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  message: {
    marginTop: 10,
    color: "red",
    textAlign: "center",
  },
})

export default Login

