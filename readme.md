## start frontend

- [ ] Накидай как с нуля установить node.js, а потом запустить фронт

```bash
docker run -it --rm -v "C:\Users\devve\Desktop\VSCode\maybe-pet\simple-todo-app\todo-app-frontend:/app" -w /app -p 3000:3000 -e WATCHPACK_POLLING=true -e HOST=0.0.0.0 node:24-slim npm start
```
