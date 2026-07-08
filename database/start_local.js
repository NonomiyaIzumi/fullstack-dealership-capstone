/**
 * Default entrypoint for this service (used both locally and on the free-tier
 * deployment): boots a real, ephemeral, in-process MongoDB via
 * mongodb-memory-server, seeds it with the demo dealers/reviews, then starts
 * the Express app against it. No external MongoDB account is required. If a
 * persistent, external MongoDB is available instead, set MONGO_URI and run
 * `npm run start:external-mongo` in place of this script.
 */
const { MongoMemoryServer } = require("mongodb-memory-server");

async function main() {
  const mongod = await MongoMemoryServer.create();
  process.env.MONGO_URI = mongod.getUri("dealershipsDB");
  console.log(`In-memory MongoDB started at ${process.env.MONGO_URI}`);

  const seed = require("./populate_mongodb");
  await seed();

  const app = require("./app");
  const PORT = process.env.PORT || 3030;
  app.listen(PORT, () => console.log(`Dealership database service listening on port ${PORT}`));

  process.on("SIGINT", async () => {
    await mongod.stop();
    process.exit(0);
  });
}

main().catch((err) => {
  console.error("Failed to start local dealership database service:", err);
  process.exit(1);
});
