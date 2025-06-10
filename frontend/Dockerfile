# 1. Node image bilan boshlaymiz
FROM node:20-alpine

# 2. Ishchi papkani belgilaymiz
WORKDIR /app

# 3. package.json va lock fayllarni nusxalaymiz
COPY package*.json ./

# 4. Paketlarni o'rnatamiz
RUN npm install

# 5. Loyiha fayllarini nusxalaymiz
COPY . .

# 6. Build qilamiz
RUN npm run build

# 7. Vite preview serverni ishlatamiz
EXPOSE 4173
CMD ["npm", "run", "preview"]
