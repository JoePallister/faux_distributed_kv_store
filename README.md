# Modulo Hashing

Run the app with module hashing with 

```uv run uvicorn app_modulo_hashing:app --reload```

Test posting key value pairs with 
```bash test scripts/post_kv_pair.sh example_key example_value```

and get the contents of the "nodes" with
```bash test scripts/get_kv_pairs.sh```

We can see the posted pairs getting distributed to the nodes based on the key hash values modulo N, where N is the number of nodes. The issue with this is 