# pull official base image
FROM node:12.18.1

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH=/app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
RUN npm install
# RUN npm install d3 d3-axis d3-format d3-scale d3-selection

# add app
COPY . ./

EXPOSE 3000

# start app
CMD ["npm", "start"]