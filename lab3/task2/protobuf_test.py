import messages_pb2

# 1. Instantiate the message class and set some attributes
pb_file = messages_pb2.file()
pb_file.id = 1
pb_file.name = "test.pdf"
pb_file.type = "application/pdf"
pb_file.size = 123

# 2. Serialize to raw bytes
encoded = pb_file.SerializeToString()
print("Message:")
print(pb_file)
print("Encoded bytes:", encoded)
print(f"Size: {len(encoded)} bytes")

# 3. Deserialize into a new message instance
pb_file_received = messages_pb2.file()
pb_file_received.ParseFromString(encoded)

# 4. Verify the reconstructed attributes match the source
assert pb_file_received.id == pb_file.id
assert pb_file_received.name == pb_file.name
assert pb_file_received.type == pb_file.type
assert pb_file_received.size == pb_file.size